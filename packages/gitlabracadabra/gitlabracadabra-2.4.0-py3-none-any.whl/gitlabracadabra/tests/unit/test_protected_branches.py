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

from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr, patch
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProtectedBranches(TestCaseWithManager):
    """Test ProtectedBranchesMixin."""

    @my_vcr.use_cassette
    def test_protected_branches_wildcard(self, cass):
        """Test new protected branch.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/protected-branches', {
            'protected_branches': {
                'release/*': {'push_access_level': 'noone', 'merge_access_level': 'maintainer'},
            },
        })
        with patch('gitlabracadabra.mixins.protected_branches.logger', autospec=True) as logger:
            self.assertEqual(project.errors(), [])
            project.process()
            self.assertTrue(cass.all_played)
            logger.warning.assert_called_once_with(
                '[%s] NOT Deleting unknown protected branch: %s (unknown_protected_branches=%s)',
                'test/protected-branches',
                'main',
                'warn',
            )

    @my_vcr.use_cassette
    def test_protected_branches_delete(self, cass):
        """Test deleting unknown protected branch.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/protected-branches2', {
            'protected_branches': {},
            'unknown_protected_branches': 'delete',
        })
        with patch('gitlabracadabra.mixins.protected_branches.logger', autospec=True) as logger:
            self.assertEqual(project.errors(), [])
            project.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with(
                '[%s] Deleting unknown protected branch: %s',
                'test/protected-branches2',
                'main',
            )

    @my_vcr.use_cassette
    def test_protected_branches_ee(self, cass):
        """Test protected branch EE.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'gitlabracadabra/test-group/protected-branches', {
            'protected_branches': {
                'main': {
                    'allowed_to_merge': [
                        {'role': 'maintainer'},
                        {'user': 'kubitus-bot'},
                        # {'group': 'some-group'},
                    ],
                    'allowed_to_push': [
                        {'role': 'noone'},
                        {'user': 'kubitus-bot'},
                        # {'group': 'some-group'},
                        # {'deploy_key': 'My Key'},
                    ],
                    'allow_force_push': True,
                    'code_owner_approval_required': True,
                },
                'develop': {
                    'allowed_to_merge': [
                        {'role': 'developer'},
                        {'user': 'kubitus-bot'},
                        # {'group': 'some-group'},
                    ],
                    'allowed_to_push': [
                        {'role': 'developer'},
                        {'user': 'kubitus-bot'},
                        # {'group': 'some-group'},
                        {'deploy_key': 'My Key'},
                    ],
                    'allow_force_push': True,
                    'code_owner_approval_required': True,
                },
            },
        })
        with patch('gitlabracadabra.mixins.protected_branches.logger', autospec=True) as logger:
            self.assertEqual(project.errors(), [])
            project.process()
            self.assertTrue(cass.all_played)
            info_calls = logger.info.mock_calls
            self.assertEqual(len(info_calls), 2)
            self.assertEqual(info_calls[0].args[0], '[%s] Creating protected branch %s: %s')
            self.assertEqual(info_calls[1].args[0], '[%s] Changing protected branch %s: %s -> %s')
            self.assertEqual(logger.warning.mock_calls, [])
