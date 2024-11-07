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

from requests import Session

from gitlabracadabra import __version__ as gitlabracadabra_version
from gitlabracadabra.packages.package_file import PackageFile


class Source:
    """Source package repository."""

    def __init__(self) -> None:
        """Initialize a Source."""
        self.session = Session()
        self.session.headers['User-Agent'] = 'gitlabracadabra/{0}'.format(gitlabracadabra_version)

    @property
    def package_files(self) -> list[PackageFile]:
        """Return list of package files.

        Raises:
            NotImplementedError: This is an abstract method.
        """
        raise NotImplementedError
