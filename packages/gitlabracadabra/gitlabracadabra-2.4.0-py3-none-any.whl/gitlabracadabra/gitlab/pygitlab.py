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

from os import getenv
from typing import TYPE_CHECKING

from gitlab import Gitlab

from requests.auth import HTTPBasicAuth

from gitlabracadabra import __version__ as gitlabracadabra_version
from gitlabracadabra.auth_info import AuthInfo
from gitlabracadabra.containers.authenticated_session import AuthenticatedSession
from gitlabracadabra.gitlab.deploy_key_cache import DeployKeyCache
from gitlabracadabra.gitlab.group_cache import GroupCache
from gitlabracadabra.gitlab.user_cache import UserCache


if TYPE_CHECKING:
    from requests import Session


class PyGitlab:
    """Python-Gitlab wrapper."""

    def __init__(
        self,
        gitlab_id: str | None,
        config_files: list[str] | None,
        debug: bool,
        auth: bool = True,
    ) -> None:
        """Initialize a Python-Gitlab wrapper.

        Args:
            gitlab_id: Section in python-gitlab config files.
            config_files: None or list of configuration files.
            debug: True to enable debugging.
            auth: True to authenticate on creation.
        """
        self._gitlab_id = gitlab_id
        self._config_files = config_files
        self._debug = debug
        options: dict[str, str | None] = {
            'server_url': getenv('GITLAB_URL'),
            'private_token': getenv('GITLAB_PRIVATE_TOKEN'),
            'oauth_token': getenv('GITLAB_OAUTH_TOKEN'),
        }
        try:
            self._gl = Gitlab.merge_config(options, self.gitlab_id, self._config_files)
        except AttributeError:
            self._gl = Gitlab.from_config(self.gitlab_id, self._config_files)
        if self.gitlab_tls_verify != '':
            self._gl.ssl_verify = self.gitlab_tls_verify
        self._gl.headers['User-Agent'] = 'gitlabracadabra/{0}'.format(gitlabracadabra_version)
        if auth:
            if self.pygitlab.private_token or self.pygitlab.oauth_token:
                self.pygitlab.auth()
        if self._debug:
            self.pygitlab.enable_debug()

        self.group_cache = GroupCache(self)
        self.user_cache = UserCache(self)
        self.deploy_key_cache = DeployKeyCache(self)

    @property
    def gitlab_id(self) -> str | None:
        """Get Gitlab id (section in python-gitlab config files).

        Returns:
            A string.
        """
        return self._gitlab_id

    @property
    def pygitlab(self) -> Gitlab:
        """Get python-gitlab object.

        Returns:
            A gitlab.Gitlab object.
        """
        return self._gl

    @property
    def registry_auth_info(self) -> AuthInfo:
        """Get Registry Authentication information.

        Returns:
            A dict, with 'headers' and 'auth' to pass to requests.

        Raises:
            ValueError: No auth info.
        """
        if self.pygitlab.private_token:
            return AuthInfo(auth=HTTPBasicAuth('personal-access-token', self.pygitlab.private_token))
        if self.pygitlab.oauth_token:
            return AuthInfo(auth=HTTPBasicAuth('oauth2', self.pygitlab.oauth_token))
        if self.pygitlab.job_token:
            return AuthInfo(auth=HTTPBasicAuth('gitlab-ci-token', self.pygitlab.job_token))
        if self.pygitlab.http_username and self.pygitlab.http_password:
            return AuthInfo(auth=HTTPBasicAuth(self.pygitlab.http_username, self.pygitlab.http_password))
        raise ValueError('No auth info')

    def registry_session_callback(self, session: AuthenticatedSession) -> None:
        """Apply options to registry session.

        Args:
            session: requests Session
        """
        session.verify = self._gl.ssl_verify
        session.auth_info = self.registry_auth_info

    def session_callback(self, session: Session) -> None:
        """Apply options to requests session.

        Args:
            session: requests Session
        """
        session.verify = self._gl.ssl_verify
        registry_auth_info = self.registry_auth_info
        session.auth = registry_auth_info.auth
        if registry_auth_info.headers is not None:
            for header_name, header_value in registry_auth_info.headers.items():
                session.headers[header_name] = header_value

    @property
    def api_url(self) -> str:
        """Get API URL.

        Returns:
            API URL.
        """
        return self.pygitlab.api_url

    @property
    def gitlab_tls_verify(self) -> bool | str:
        """Get TLS verify.

        Returns:
            Boolean to enable or disable, string for CA path, empty string to keep default.
        """
        gitlab_tls_verify = getenv('GITLAB_TLS_VERIFY', '')
        if gitlab_tls_verify in {'true', 'false'}:
            return gitlab_tls_verify == 'true'
        return gitlab_tls_verify
