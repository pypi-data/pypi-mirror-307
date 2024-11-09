# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2022 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import logging
from os.path import isdir
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from pygit2 import GIT_FETCH_PRUNE, GitError, RemoteCallbacks, Repository, init_repository

from gitlabracadabra.disk_cache import cache_dir
from gitlabracadabra.gitlab.connections import GitlabConnections
from gitlabracadabra.matchers import Matcher
from gitlabracadabra.objects.object import GitLabracadabraObject


if TYPE_CHECKING:
    from pygit2 import Reference


GITLAB_REMOTE_NAME = 'gitlab'
MIRROR_PARAM_URL = 'url'
MIRROR_DIRECTION_PULL = 'pull'
MIRROR_REMOTE_NAME_PULL = 'pull'
PUSH_OPTIONS = 'push_options'

logger = logging.getLogger(__name__)


class MirrorsMixin(GitLabracadabraObject):
    """Object with mirrors."""

    def _process_mirrors(
        self,
        param_name: str,
        param_value: Any,
        dry_run: bool = False,
        skip_save: bool = False,
    ) -> None:
        """Process the mirrors param.

        Args:
            param_name: "mirrors".
            param_value: List of mirror dicts.
            dry_run: Dry run.
            skip_save: False.
        """
        assert param_name == 'mirrors'  # noqa: S101
        assert not skip_save  # noqa: S101

        pull_mirror_count = 0
        self._init_repo()
        self._fetch_remote(
            GITLAB_REMOTE_NAME,
            self.connection.pygit2_remote_callbacks,
        )
        for mirror in param_value:
            direction = mirror.get('direction', MIRROR_DIRECTION_PULL)
            push_options = mirror.get(PUSH_OPTIONS, [])
            if 'skip_ci' in mirror:
                push_options.append('ci.skip')
            if direction == MIRROR_DIRECTION_PULL:
                if pull_mirror_count > 0:
                    logger.warning(
                        '[%s] NOT Pulling mirror: %s (Only first pull mirror is processed)',
                        self._name,
                        mirror[MIRROR_PARAM_URL],
                    )
                    continue
                self._pull_mirror(mirror, push_options, dry_run)
                pull_mirror_count += 1
            else:
                logger.warning(
                    '[%s] NOT Pushing mirror: %s (Not supported yet)',
                    self._name,
                    mirror[MIRROR_PARAM_URL],
                )

    def _init_repo(self) -> None:
        """Init the cache repository."""
        web_url_slug = quote(self.web_url(), safe='')
        repo_dir = str(cache_dir('') / web_url_slug)
        if isdir(repo_dir):
            self._repo = Repository(repo_dir)
        else:
            logger.debug(
                '[%s] Creating cache repository in %s',
                self._name,
                repo_dir,
            )
            self._repo = init_repository(repo_dir, bare=True)
        try:
            self._repo.remotes[GITLAB_REMOTE_NAME]  # noqa: WPS428
        except KeyError:
            self._repo.remotes.create(
                GITLAB_REMOTE_NAME,
                self.web_url(),
                '+refs/heads/*:refs/remotes/gitlab/heads/*',
            )
            self._repo.remotes.add_fetch(GITLAB_REMOTE_NAME, '+refs/tags/*:refs/remotes/gitlab/tags/*')
            self._repo.remotes.add_push(GITLAB_REMOTE_NAME, '+refs/heads/*:refs/heads/*')
            self._repo.remotes.add_push(GITLAB_REMOTE_NAME, '+refs/tags/*:refs/tags/*')
            self._repo.config['remote.gitlab.mirror'] = True

    def _fetch_remote(
        self,
        name: str,
        remote_callbacks: RemoteCallbacks | None = None,
    ) -> None:
        """Fetch the repo with the given name.

        Args:
            name: Remote name.
            remote_callbacks: Credentials and certificate check as pygit2.RemoteCallbacks.
        """
        remote = self._repo.remotes[name]
        try:
            # https://gitlab.com/gitlabracadabra/gitlabracadabra/-/issues/25
            remote.fetch(
                refspecs=remote.fetch_refspecs,
                callbacks=remote_callbacks,
                prune=GIT_FETCH_PRUNE,
                proxy=True,
            )
        except TypeError:
            # proxy arg in pygit2 1.6.0
            logger.warning(
                '[%s] Ignoring proxy for remote=%s refs=%s: requires pygit2>=1.6.0',
                self._name,
                name,
                ','.join(remote.fetch_refspecs),
            )
            remote.fetch(
                refspecs=remote.fetch_refspecs,
                callbacks=remote_callbacks,
                prune=GIT_FETCH_PRUNE,
            )

    def _pull_mirror(self, mirror: dict, push_options: list[str], dry_run: bool) -> None:
        """Pull from the given mirror and push.

        Args:
            mirror: Current mirror dict.
            push_options: push options.
            dry_run: Dry run.
        """
        try:
            self._repo.remotes[MIRROR_REMOTE_NAME_PULL]  # noqa: WPS428
        except KeyError:
            self._repo.remotes.create(
                MIRROR_REMOTE_NAME_PULL,
                mirror[MIRROR_PARAM_URL],
                '+refs/heads/*:refs/heads/*',
            )
            self._repo.remotes.add_fetch(MIRROR_REMOTE_NAME_PULL, '+refs/tags/*:refs/tags/*')
            self._repo.config['remote.pull.mirror'] = True
        remote_callbacks = None
        pull_auth_id = mirror.get('auth_id')
        if pull_auth_id:
            remote_callbacks = GitlabConnections().get_connection(pull_auth_id).pygit2_remote_callbacks
        self._fetch_remote(MIRROR_REMOTE_NAME_PULL, remote_callbacks)
        for ref in self._repo.references.objects:
            self._sync_ref(mirror, ref, push_options, dry_run)

    def _sync_ref(  # noqa: WPS210 WPS231
        self,
        mirror: dict,
        ref: Reference,
        push_options: list[str],
        dry_run: bool,
    ) -> None:
        """Synchronize the given branch or tag.

        Args:
            mirror: Current mirror dict.
            ref: reference objects.
            push_options: push options.
            dry_run: Dry run.
        """
        if ref.name.startswith('refs/heads/'):
            ref_type = 'head'
            ref_type_human = 'branch'
            ref_type_human_plural = 'branches'
        elif ref.name.startswith('refs/tags/'):
            ref_type = 'tag'
            ref_type_human = 'tag'
            ref_type_human_plural = 'tags'
        else:
            return
        shorthand = ref.name.split('/', 2)[2]

        # Ref mapping
        dest_shortand = shorthand
        if ref_type_human_plural in mirror:
            dest_shortand = None
            mappings: list[dict[str, str | list[str]]] = mirror.get(ref_type_human_plural)  # type: ignore
            for mapping in mappings:
                matcher = Matcher(
                    mapping.get('from', ''),
                    None,
                    log_prefix='[{0}] {1} {2}'.format(
                        self._name,
                        mirror[MIRROR_PARAM_URL],
                        ref_type_human_plural,
                    ),
                )
                matches = matcher.match([shorthand])
                if matches:
                    to_param = mapping.get('to', shorthand)
                    dest_shortand = matches[0].expand(to_param)
                    push_options = mapping.get(PUSH_OPTIONS, push_options)  # type: ignore
                    break

        if dest_shortand is None:
            return

        pull_commit = ref.peel().id
        gitlab_ref = self._repo.references.get(
            'refs/remotes/gitlab/{ref_type}s/{ref}'.format(ref_type=ref_type, ref=dest_shortand),
        )
        try:
            gitlab_commit = gitlab_ref.peel().id
        except AttributeError:
            gitlab_commit = None
        if pull_commit == gitlab_commit:
            return
        if dry_run:
            logger.info(
                '[%s] %s NOT Pushing %s %s to %s: %s -> %s (dry-run)',
                self._name,
                mirror[MIRROR_PARAM_URL],
                ref_type_human,
                shorthand,
                dest_shortand,
                gitlab_commit,
                str(pull_commit),
            )
            return
        logger.info(
            '[%s] %s Pushing %s %s to %s: %s -> %s',
            self._name,
            mirror[MIRROR_PARAM_URL],
            ref_type_human,
            shorthand,
            dest_shortand,
            gitlab_commit,
            str(pull_commit),
        )
        refspec = '{ref_name}:refs/{ref_type}s/{ref}'.format(
            ref_name=ref.name,
            ref_type=ref_type,
            ref=dest_shortand,
        )
        try:
            self._push_remote(
                GITLAB_REMOTE_NAME,
                [refspec],
                push_options,
                self.connection.pygit2_remote_callbacks,
            )
        except GitError as err:
            logger.error(  # noqa: G200
                '[%s] Unable to push remote=%s refs=%s: %s',
                self._name,
                GITLAB_REMOTE_NAME,
                refspec,
                err,
            )

    def _push_remote(
        self,
        name: str,
        refs: list[str],
        push_options: list[str],
        remote_callbacks: RemoteCallbacks | None,
    ) -> None:
        """Push to the repo with the given name.

        Args:
            name: Remote name.
            refs: refs list.
            push_options: push options.
            remote_callbacks: Credentials and certificate check as pygit2.RemoteCallbacks.
        """
        remote = self._repo.remotes[name]
        kwargs = {
            'specs': refs,
            'callbacks': remote_callbacks,
            'proxy': True,
        }
        if push_options:
            kwargs[PUSH_OPTIONS] = push_options
            try:
                remote.push(**kwargs)
                return
            except TypeError:
                # push_options arg in pygit2 1.16.0
                logger.warning(
                    '[%s] Ignoring push options %s for remote=%s refs=%s: requires pygit2>=1.16.0',
                    self._name,
                    ','.join(push_options),
                    name,
                    ','.join(refs),
                )
                kwargs.pop(PUSH_OPTIONS)
        try:
            remote.push(**kwargs)
        except TypeError:
            # proxy arg in pygit2 1.6.0
            logger.warning(
                '[%s] Ignoring proxy for remote=%s refs=%s: requires pygit2>=1.6.0',
                self._name,
                name,
                ','.join(refs),
            )
            kwargs.pop('proxy')
            remote.push(**kwargs)
