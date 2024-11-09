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
from urllib.parse import urlparse

from pygit2 import Passthrough, RemoteCallbacks, UserPass

from gitlabracadabra.gitlab.pygitlab import PyGitlab


if TYPE_CHECKING:
    from pygit2.enums import CredentialType


class PyGit2(PyGitlab):
    """PyGit2 wrapper."""

    def pygit2_certificate_check(self, _certificate: None, valid: bool, host: str | bytes) -> bool:
        """Check certificate.

        Args:
            _certificate: Currently always None.
            valid: Whether the TLS/SSH library thinks the certificate is valid.
            host: The hostname we want to connect to.

        Returns:
            True to connect, False to abort.

        Raises:
            Passthrough: Use default behavior.
        """
        if self.pygitlab.ssl_verify is True:
            raise Passthrough
        if self.pygitlab.ssl_verify is False:
            allowed_host = urlparse(self.api_url).hostname
            if allowed_host is not None and host in {allowed_host, allowed_host.encode()}:
                return True
            raise Passthrough
        # self.pygitlab.ssl_verify is a CA path, no way to verify
        return False

    def pygit2_credentials(self, url: str, _username_from_url: str | None, _allowed_types: CredentialType) -> UserPass:
        """Get PyGit2 credentials.

        Args:
            url: The url of the remote.
            _username_from_url: Username extracted from the url, if any.
            _allowed_types: Combination of bitflags representing the credential types supported by the remote.

        Returns:
            A pygit2.UserPass.

        Raises:
            ValueError: No credentials found.
        """
        target_hostname = urlparse(url).hostname
        allowed_hostname = urlparse(self.api_url).hostname
        if allowed_hostname != target_hostname:
            raise ValueError(
                'Target hostname {0} not matching allowed hostname {1}'.format(
                    target_hostname,
                    allowed_hostname,
                ),
            )
        if self.pygitlab.private_token:
            return UserPass('oauth2', self.pygitlab.private_token)
        if self.pygitlab.oauth_token:
            return UserPass('oauth2', self.pygitlab.oauth_token)
        if self.pygitlab.job_token:
            return UserPass('gitlab-ci-token', self.pygitlab.job_token)
        if self.pygitlab.http_username and self.pygitlab.http_password:
            return UserPass(self.pygitlab.http_username, self.pygitlab.http_password)
        raise ValueError('No PyGit2 credentials for {target_hostname}')

    @property
    def pygit2_remote_callbacks(self) -> RemoteCallbacks:
        """Get PyGit2 RemoteCallbacks.

        Returns:
            A pygit2.RemoteCallbacks.
        """
        cb = RemoteCallbacks()
        cb.credentials = self.pygit2_credentials
        if self.pygitlab.ssl_verify is not True:
            cb.certificate_check = self.pygit2_certificate_check
        return cb
