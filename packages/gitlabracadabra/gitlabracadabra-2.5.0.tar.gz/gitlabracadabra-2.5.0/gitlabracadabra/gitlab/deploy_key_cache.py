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

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from gitlabracadabra.gitlab.pygitlab import PyGitlab


class DeployKeyCache:
    """Deploy keys mapping cache.

    indexed by id and slug (tile@project_id).
    """

    def __init__(self, connection: PyGitlab) -> None:
        """Initialize a deploy keys cache.

        Args:
            connection: A GitlabConnection/PyGitlab.
        """
        self._connection = connection
        self._slug2id: dict[str, int | None] = {}
        self._id2slug: dict[int, str | None] = {}

    def map_deploy_key(self, deploy_key_id: int, project_id: int, deploy_key_title: str) -> None:
        """Map deploy key id and slug.

        Args:
            deploy_key_id: Deploy key id.
            project_id: GitLab Project id.
            deploy_key_title: Deploy key title.
        """
        slug = '{0}@{1}'.format(deploy_key_title, project_id)
        self._id2slug[deploy_key_id] = slug
        self._slug2id[slug] = deploy_key_id

    def id_from_title(self, project_id: int, deploy_key_title: str) -> int | None:
        """Get deploy key id from project and deploy key title.

        Args:
            project_id: GitLab Project id.
            deploy_key_title: Deploy key title.

        Returns:
            Deploy key id.
        """
        slug = '{0}@{1}'.format(deploy_key_title, project_id)
        if slug not in self._slug2id:
            self._slug2id[slug] = None
            project = self._connection.pygitlab.projects.get(project_id, lazy=True)
            for deploy_key in project.keys.list(all=True):
                if deploy_key.title == deploy_key_title:
                    self._slug2id[slug] = deploy_key.id
                    self.map_deploy_key(deploy_key.id, project_id, deploy_key_title)
                    break
        return self._slug2id[slug]
