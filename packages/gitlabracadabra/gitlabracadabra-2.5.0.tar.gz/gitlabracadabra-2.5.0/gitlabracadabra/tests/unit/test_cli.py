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
from unittest import TestCase
from unittest.mock import patch

from gitlabracadabra.cli import ExitCodeHandler, main
from gitlabracadabra.objects.project import logger as project_logger
from gitlabracadabra.tests import patch_open


class TestExitCodeHandler(TestCase):
    """Test ExitCodeHandler."""

    def test_exit_code_handler(self):
        """Test ExitCodeHandler."""
        exit_code_handler = ExitCodeHandler()
        logger = logging.getLogger('foobar')
        logger.addHandler(exit_code_handler)
        self.assertEqual(exit_code_handler.max_levelno, logging.NOTSET)
        logger.warning('Some warning')
        self.assertEqual(exit_code_handler.max_levelno, logging.WARNING)
        logger.error('Some error')
        self.assertEqual(exit_code_handler.max_levelno, logging.ERROR)


class TestCli:
    """Test cli."""

    def test_main(self, caplog):
        """Test main function.

        Args:
            caplog: pytest caplog fixture.
        """
        with caplog.at_level(logging.INFO):
            gitlabracadabra_content = """
                    group/project:
                      visibility: public
                    """
            contents_map = {
                'gitlabracadabra.yml': gitlabracadabra_content,
            }
            err_code = 0
            try:
                with patch_open(contents_map):
                    with patch('gitlabracadabra.gitlab.connection.GitlabConnection', autospec=True) as connection:
                        with patch('gitlabracadabra.objects.project.GitLabracadabraProject', autospec=True) as project:
                            connection.pygitlab.projects.get.return_value = {
                                'visibility': 'private',
                            }
                            project.return_value.process.side_effect = self._add_some_warn
                            main(['--fail-on-warnings'])
                            assert project.call_args == (('gitlabracadabra.yml', 'group/project', {'visibility': 'public'}))
            except SystemExit as err:
                err_code = err.code
            assert err_code == 1
            assert caplog.record_tuples == [
                ('gitlabracadabra.objects.project', logging.WARNING, 'Some warning'),
            ]

    def _add_some_warn(self, *args, **kwargs):
        project_logger.warning('Some warning')
