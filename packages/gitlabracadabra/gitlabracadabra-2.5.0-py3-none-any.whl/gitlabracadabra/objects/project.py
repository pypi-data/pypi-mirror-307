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

import logging

from gitlab.exceptions import GitlabListError

from gitlabracadabra.gitlab.access_levels import access_level_value
from gitlabracadabra.mixins.boards import BoardsMixin
from gitlabracadabra.mixins.groups import GroupsMixin
from gitlabracadabra.mixins.image_mirrors import ImageMirrorsMixin
from gitlabracadabra.mixins.labels import LabelsMixin
from gitlabracadabra.mixins.members import MembersMixin
from gitlabracadabra.mixins.milestones import MilestonesMixin
from gitlabracadabra.mixins.mirrors import MirrorsMixin
from gitlabracadabra.mixins.package_mirrors import PackageMirrorsMixin
from gitlabracadabra.mixins.pipeline_schedules import PipelineSchedulesMixin
from gitlabracadabra.mixins.protected_branches import ProtectedBranchesMixin
from gitlabracadabra.mixins.rename_branches import RenameBranchesMixin
from gitlabracadabra.mixins.variables import VariablesMixin
from gitlabracadabra.mixins.webhooks import WebhooksMixin
from gitlabracadabra.objects.object import GitLabracadabraObject


logger = logging.getLogger(__name__)


class GitLabracadabraProject(BoardsMixin, GroupsMixin, ImageMirrorsMixin, LabelsMixin,
                             MembersMixin, MilestonesMixin, MirrorsMixin, PackageMirrorsMixin, PipelineSchedulesMixin,
                             ProtectedBranchesMixin, RenameBranchesMixin, VariablesMixin, WebhooksMixin,
                             GitLabracadabraObject):
    EXAMPLE_YAML_HEADER = 'mygroup/myproject:\n'
    DOC = [
        '# Project lifecycle',
        'gitlab_id',
        'create_object',
        'delete_object',
        'initialize_with_readme',
        'repository_object_format',


        '# Manage',
        '## Members',
        'members',
        'unknown_members',
        'groups',
        'unknown_groups',

        '## Labels',
        'labels',
        'unknown_labels',


        '# Plan',
        '## Issue boards',
        'boards',
        'unknown_boards',
        'unknown_board_lists',

        '## Milestones',
        'milestones',
        'unknown_milestones',

        # '## Iterations',


        '# Code',
        '## Branches',
        'branches',
        'rename_branches',


        '# Build',
        '## Pipeline schedules',
        'pipeline_schedules',
        'unknown_pipeline_schedules',
        'unknown_pipeline_schedule_variables',


        '# Settings',
        '## General Settings',
        '### Naming, description, topics',
        'name',
        'description',
        'topics',
        # 'avatar',  # FIXME Gitlabracadabra

        '### Visibility, project features, permissions',
        'visibility',
        'request_access_enabled',
        'issues_access_level',
        # 'cve_id_request_enabled',  # FIXME GitLab
        'repository_access_level',
        'merge_requests_access_level',
        'forking_access_level',
        'lfs_enabled',
        'builds_access_level',
        'container_registry_access_level',
        'analytics_access_level',
        'requirements_access_level',
        'security_and_compliance_access_level',
        'wiki_access_level',
        'snippets_access_level',
        'packages_enabled',
        'model_experiments_access_level',
        'model_registry_access_level',
        'pages_access_level',
        'monitor_access_level',
        'environments_access_level',
        'feature_flags_access_level',
        'infrastructure_access_level',
        'releases_access_level',
        # 'duo_features_enabled',  # FIXME Gitlab
        'emails_enabled',
        # 'show_diff_preview_in_email',  # FIXME Gitlab
        # 'show_default_award_emojis',  # FIXME Gitlab
        # 'ci_resources_enabled',  # FIXME Gitlab

        # '### Badges',

        '### Default description template for issues',
        'issues_template',

        '### Service Desk',
        'service_desk_enabled',
        # 'service_desk_...',  # FIXME Gitlab

        '### Advanced',
        'archived',

        # '## Integrations',  # FIXME

        '## Webhooks',
        'webhooks',
        'unknown_webhooks',

        '## Repository',
        '### Branch defaults',
        'default_branch',
        'autoclose_referenced_issues',
        'issue_branch_template',

        # '### Branch Rules',  # FIXME ...

        # '### Push Rules',  # FIXME ...

        '### Mirroring repositories',
        'mirror',
        'import_url',
        'mirror_user_id',
        'mirror_overwrites_diverged_branches',
        'mirror_trigger_builds',
        'only_mirror_protected_branches',

        '### Protected Branches',
        'protected_branches',
        'unknown_protected_branches',

        '### Protected Tags',
        'protected_tags',
        'unknown_protected_tags',

        # '### Deploy Keys',  # FIXME ...

        # '### Deploy Tokens',  # FIXME ...

        '## Merge requests',
        '### Merge requests',
        'merge_method',
        'merge_pipelines_enabled',
        'merge_trains_enabled',
        # 'merge_trains_skip_train_allowed',  # FIXME GitLab
        'resolve_outdated_diff_discussions',
        'printing_merge_request_link_enabled',
        'remove_source_branch_after_merge',
        'squash_option',
        'only_allow_merge_if_pipeline_succeeds',
        'allow_merge_on_skipped_pipeline',
        'only_allow_merge_if_all_discussions_are_resolved',
        'only_allow_merge_if_all_status_checks_passed',
        'suggestion_commit_message',
        'merge_commit_template',
        'squash_commit_template',
        'merge_requests_template',

        '### Merge request approvals',  # FIXME ...
        'approvals_before_merge',

        '## CI / CD Settings',
        '### General pipelines',
        'public_jobs',
        'auto_cancel_pending_pipelines',
        'ci_forward_deployment_enabled',
        'ci_forward_deployment_rollback_allowed',
        'ci_separated_caches',
        'ci_restrict_pipeline_cancellation_role',
        'ci_config_path',
        'build_git_strategy',
        'ci_default_git_depth',
        'build_timeout',
        'ci_allow_fork_pipelines_to_run_in_parent_project',

        '### Auto DevOps',
        'auto_devops_enabled',
        'auto_devops_deploy_strategy',

        '### Protected Environments',
        # FIXME ...
        'allow_pipeline_trigger_approve_deployment',

        '### Runners',
        'shared_runners_enabled',
        'group_runners_enabled',

        '### Artifacts',
        'keep_latest_artifact',

        '### Variables',
        'variables',
        'unknown_variables',

        # '### Pipeline trigger tokens',  # FIXME

        # '### Automatic deployment rollbacks',  # FIXME
        # 'auto_rollback_enabled',  # FIXME GitLab

        # '### Deploy freezes',  # FIXME

        # '### Job token permissions',  # FIXME

        # '### Secure files',  # FIXME

        # '### Pipeline subscriptions',  # FIXME


        '## Packages and registries',
        '### Cleanup policies',
        'container_expiration_policy',

        '# Mirroring repositories, packages and container images',
        'mirrors',
        'package_mirrors',
        'image_mirrors',

        '# Deprecated',
        'build_coverage_regex',
        'container_registry_enabled',
        'emails_disabled',
        'issues_enabled',
        'jobs_enabled',
        'merge_requests_enabled',
        'public_builds',
        'snippets_enabled',
        'tag_list',
        'wiki_enabled',
    ]
    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Project',
        'type': 'object',
        'properties': {
            'gitlab_id': {
                'type': 'string',
                'description': 'GitLab id',
                '_example': 'gitlab',
                '_doc_link': 'action_file.md#gitlab_id',
            },
            'create_object': {
                'type': 'boolean',
                'description': 'Create object if it does not exists',
            },
            'delete_object': {
                'type': 'boolean',
                'description': 'Delete object if it exists',
            },

            # From https://docs.gitlab.com/ee/api/projects.html#create-project
            # and https://docs.gitlab.com/ee/api/projects.html#edit-project
            'initialize_with_readme': {
                'type': 'boolean',
                'description': 'false by default',
            },
            'repository_object_format': {
                'type': 'string',
                'description': 'Repository object format',
                'enum': ['sha1', 'sha256'],
            },

            # From https://docs.gitlab.com/ee/api/members.html#add-a-member-to-a-group-or-project
            # FIXME expires_at not supported
            'members': {
                'type': 'object',
                'description': 'Members',
                'additionalProperties': {
                    'type': 'string',
                    'description': 'The permissions level to grant the member.',
                    'enum': ['guest', 'reporter', 'developer', 'maintainer', 'owner'],
                },
                '_example': ('\n'
                             '    foo: developer\n'
                             '    bar: maintainer # one of guest, reporter, developer, maintainer, owner\n'),
            },
            'unknown_members': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown members (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/projects.html#share-project-with-group_access_level
            # and https://docs.gitlab.com/ee/api/projects.html#delete-a-shared-project-link-within-a-group
            # FIXME expires_at not supported
            'groups': {
                'type': 'object',
                'description': 'Groups',
                'additionalProperties': {
                    'type': 'string',
                    'description': 'The permissions level to grant the group.',
                    'enum': ['guest', 'reporter', 'developer', 'maintainer'],
                },
                '_example': ('\n'
                             '    group/foo: guest\n'
                             '    group/bar: reporter # one of guest, reporter, developer, maintainer\n'),
            },
            'unknown_groups': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown groups (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },

            # From https://docs.gitlab.com/ee/api/labels.html#create-a-new-label
            'labels': {
                'type': 'array',
                'description': "The list of project's labels",
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the label.',
                        },
                        'color': {
                            'type': 'string',
                            'description': 'The color of the label.',
                        },
                        'description': {
                            'type': 'string',
                            'description': 'The description of the label.',
                        },
                        'priority': {
                            'type': 'integer',
                            'description': 'The priority of the label.',
                        },
                    },
                    'required': ['name'],  # color not required to allow priority override
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - name: critical\n'
                             '      priority: 0\n'
                             '    - name: bug\n'
                             '      priority: 1\n'
                             '    - name: confirmed\n'
                             '      priority: 2\n'),
            },
            'unknown_labels': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown labels (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },

            # From https://docs.gitlab.com/ee/api/boards.html
            'boards': {
                'type': 'array',
                'description': "The list of project's boards",
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the board.',
                        },
                        'old_name': {
                            'type': 'string',
                            'description': 'The previous name of the board.',
                        },
                        'hide_backlog_list': {
                            'type': 'boolean',
                            'description': 'Hide the Open list',
                        },
                        'hide_closed_list': {
                            'type': 'boolean',
                            'description': 'Hide the Closed list',
                        },
                        'lists': {
                            'type': 'array',
                            'description': 'Ordered list of labels',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'label': {
                                        'type': 'string',
                                        'description': 'The name of a label',
                                    },
                                },
                            },
                        },
                        'unknown_lists': {  # GitLabracadabra
                            'type': 'string',
                            'description': ('What to do with unknown board lists '
                                            '(Value of `unknown_board_lists` by default).'),
                            'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
                        },
                    },
                    'required': ['name'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - name: My Board\n'
                             '      # old_name: Development # Use this to rename a board\n'
                             '      hide_backlog_list: false\n'
                             '      hide_closed_list: false\n'
                             '      lists:\n'
                             '        - label: TODO\n'
                             '        - label: WIP\n'),
            },
            'unknown_boards': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown boards (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            'unknown_board_lists': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown board lists (`delete` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },

            # From https://docs.gitlab.com/ee/api/milestones.html#edit-milestone
            'milestones': {
                'type': 'array',
                'description': "The list of project's milestones",
                'items': {
                    'type': 'object',
                    'properties': {
                        'title': {
                            'type': 'string',
                            'description': 'The title of a milestone',
                        },
                        'description': {
                            'type': 'string',
                            'description': 'The description of a milestone',
                        },
                        'due_date': {
                            'type': 'string',
                            'description': 'The due date of the milestone',
                            'pattern': '^(\\d{4}-\\d{2}-\\d{2})?$',
                        },
                        'start_date': {
                            'type': 'string',
                            'description': 'The start date of the milestone',
                            'pattern': '^(\\d{4}-\\d{2}-\\d{2})?$',
                        },
                        'state': {
                            'type': 'string',
                            'description': 'The state event of the milestone',
                            'enum': ['closed', 'active'],
                        },
                    },
                    'required': ['title'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             "    - title: '1.0'\n"
                             '      description: Version 1.0\n'
                             "      due_date: '2021-01-23' # Quotes are mandatory\n"
                             "      start_date: '2020-01-23' # Quotes are mandatory\n"
                             '      state: active # or closed\n'),
            },
            'unknown_milestones': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown milestones (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },

            # From https://docs.gitlab.com/ee/api/branches.html#create-repository-branch
            'branches': {
                'type': 'array',
                'description': 'The list of branches for a project. '
                               'Branches are created in order',
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - main\n'
                             '    - develop'),
            },
            'rename_branches': {
                'type': 'array',
                'description': 'Rename branches of a project. '
                               'Rename pairs (old_name: new_name) are processed in order',
                'items': {
                    'type': 'object',
                    'additionalProperties': {
                        'type': 'string',
                        'description': 'The new branch name.',
                    },
                    'minProperties': 1,
                    'maxProperties': 1,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - old_name: new_name\n'
                             '    # To Rename consecutive branches:\n'
                             '    - branch2: branch3\n'
                             '    - branch1: branch2'),
            },

            # From https://docs.gitlab.com/ee/api/pipeline_schedules.html#create-a-new-pipeline-schedule
            'pipeline_schedules': {
                'type': 'array',
                'description': "The list of project's pipeline schedules",
                'items': {
                    'type': 'object',
                    'properties': {
                        'description': {
                            'type': 'string',
                            'description': 'The description of pipeline schedule',
                            'pattern': '[a-zA-Z0-9_]+',
                        },
                        'ref': {
                            'type': 'string',
                            'description': 'The branch/tag name will be triggered',
                        },
                        'cron': {
                            'type': 'string',
                            'description': ('The cron (e.g. `0 1 * * *`) '
                                            '([Cron syntax](https://en.wikipedia.org/wiki/Cron))'),
                        },
                        'cron_timezone': {
                            'type': 'string',
                            'description': ('The timezone supported by `ActiveSupport::TimeZone` '
                                            "(e.g. `Pacific Time (US & Canada)`) (default: `'UTC'`)"),
                        },
                        'active': {
                            'type': 'boolean',
                            'description': 'The activation of pipeline schedule',
                        },
                        # From https://docs.gitlab.com/ee/api/pipeline_schedules.html
                        # #create-a-new-pipeline-schedule-variable
                        'variables': {
                            'type': 'array',
                            'description': "The list of project's variables",
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'key': {
                                        'type': 'string',
                                        'description': 'The key of a variable',
                                        'pattern': '[a-zA-Z0-9_]+',
                                    },
                                    'value': {
                                        'type': 'string',
                                        'description': 'The value of a variable',
                                    },
                                    'variable_type': {
                                        'type': 'string',
                                        'description': ('The type of a variable. '
                                                        'Available types are: env_var (default) and file'),
                                        'enum': ['env_var', 'file'],
                                    },
                                },
                                'required': ['key', 'value'],
                                'additionalProperties': False,
                            },
                            'uniqueItems': True,
                        },
                        'unknown_variables': {  # GitLabracadabra
                            'type': 'string',
                            'description': ('What to do with unknown pipeline schedule variables '
                                            '(Value of `unknown_pipeline_schedule_variables` by default).'),
                            'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
                        },
                    },
                    'required': ['description', 'ref', 'cron'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - description: Build packages\n'
                             '      ref: main\n'
                             "      cron: '0 1 * * 5'\n"
                             '      # cron_timezone: UTC\n'
                             '      # active: true\n'
                             '      variables:\n'
                             '        - key: MY_VAR\n'
                             '          value: my value\n'
                             '          # variable_type: env_var # or file\n'
                             '      # unknown_variables: warn # one of warn, delete, remove, ignore, skip\n'),
            },
            'unknown_pipeline_schedules': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown pipeline schedules (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            'unknown_pipeline_schedule_variables': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown pipeline schedule variables (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },

            'name': {
                'type': 'string',
                'description': 'Project name',
            },
            # 'path': {
            #     'type': 'string',
            #     'description': 'Repository name for new project. '
            #                    'Generated based on name if not provided (generated lowercased with dashes).',
            # },
            'description': {
                'type': 'string',
                'description': 'Project description',
                '_example': '|-\n    🧹 GitLabracadabra 🧙\n\n    :alembic: Adds some magic to GitLab :crystal\\_ball:',
            },
            'topics': {
                'type': 'array',
                'description': 'Topics',
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
                '_example': '[GitLab, API, YAML]',
            },
            # 'avatar': {
            #     'type': 'string',
            #     'description': 'Project avatar',
            # },
            'visibility': {
                'type': 'string',
                'description': 'Project visibility',
                'enum': ['private', 'internal', 'public'],
            },
            'request_access_enabled': {
                'type': 'boolean',
                'description': 'Allow users to request access',
            },
            'issues_access_level': {
                'type': 'string',
                'description': 'Set visibility of issues.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'repository_access_level': {
                'type': 'string',
                'description': 'Set visibility of repository.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'merge_requests_access_level': {
                'type': 'string',
                'description': 'Set visibility of merge requests.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'forking_access_level': {
                'type': 'string',
                'description': 'Set visibility of forks.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'lfs_enabled': {
                'type': 'boolean',
                'description': 'Enable LFS',
            },
            'builds_access_level': {
                'type': 'string',
                'description': 'Set visibility of pipelines.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'container_registry_access_level': {
                'type': 'string',
                'description': 'Set visibility of container registry.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'analytics_access_level': {
                'type': 'string',
                'description': 'Set visibility of analytics.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'requirements_access_level': {
                'type': 'string',
                'description': 'Set visibility of requirements management.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'security_and_compliance_access_level': {
                'type': 'string',
                'description': 'Set visibility of security and compliance.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'wiki_access_level': {
                'type': 'string',
                'description': 'Set visibility of wiki.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'snippets_access_level': {
                'type': 'string',
                'description': 'Set visibility of snippets.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'packages_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable packages repository feature',
            },
            'model_experiments_access_level': {
                'type': 'string',
                'description': 'Set visibility of machine learning model experiments.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'model_registry_access_level': {
                'type': 'string',
                'description': 'Set visibility of machine learning model registry.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'pages_access_level': {
                'type': 'string',
                'description': 'Set visibility of GitLab Pages.',
                'enum': ['disabled', 'private', 'enabled', 'public'],
            },
            'monitor_access_level': {
                'type': 'string',
                'description': 'Set visibility of application performance monitoring.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'environments_access_level': {
                'type': 'string',
                'description': 'Set visibility of environments.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'feature_flags_access_level': {
                'type': 'string',
                'description': 'Set visibility of feature flags.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'infrastructure_access_level': {
                'type': 'string',
                'description': 'Set visibility of infrastructure management.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'releases_access_level': {
                'type': 'string',
                'description': 'Set visibility of releases.',
                'enum': ['disabled', 'private', 'enabled'],
            },
            'emails_enabled': {
                'type': 'boolean',
                'description': 'Enable email notifications.',
            },
            'issues_template': {
                'type': 'string',
                'description': 'Default description for Issues.',
            },
            'service_desk_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable Service Desk feature.',
            },
            # https://docs.gitlab.com/ee/api/projects.html#archive-a-project
            # https://docs.gitlab.com/ee/api/projects.html#unarchive-a-project
            'archived': {
                'type': 'boolean',
                'description': 'Archive or unarchive project',
            },

            # From https://docs.gitlab.com/ee/api/projects.html#hooks
            'webhooks': {
                'type': 'array',
                'description': "The list of project's webhooks",
                'items': {
                    'type': 'object',
                    'properties': {
                        'url': {
                            'type': 'string',
                            'description': 'The hook URL',
                        },
                        'push_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on push events',
                        },
                        'push_events_branch_filter': {
                            'type': 'string',
                            'description': 'Trigger hook on push events for matching branches only',
                        },
                        'issues_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on issues events',
                        },
                        'confidential_issues_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on confidential issues events',
                        },
                        'merge_requests_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on merge requests events',
                        },
                        'tag_push_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on tag push events',
                        },
                        'note_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on note events',
                        },
                        'confidential_note_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on confidential note events',
                        },
                        'job_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on job events',
                        },
                        'pipeline_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on pipeline events',
                        },
                        'wiki_page_events': {
                            'type': 'boolean',
                            'description': 'Trigger hook on wiki events',
                        },
                        'enable_ssl_verification': {
                            'type': 'boolean',
                            'description': 'Do SSL verification when triggering the hook',
                        },
                        'token': {
                            'type': 'string',
                            'description': ('Secret token to validate received payloads; '
                                            'this will not be returned in the response'),
                        },
                    },
                    'required': ['url'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - url: http://example.com/api/trigger\n'
                             '      push_events: true\n'
                             "      push_events_branch_filter: ''\n"
                             '      issues_events: true\n'
                             '      confidential_issues_events: true\n'
                             '      merge_requests_events: true\n'
                             '      tag_push_events: true\n'
                             '      note_events: true\n'
                             '      confidential_note_events: true\n'
                             '      job_events: true\n'
                             '      pipeline_events: true\n'
                             '      wiki_page_events: true\n'
                             '      enable_ssl_verification: true\n'
                             '      # token: T0k3N\n'),
            },
            'unknown_webhooks': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown webhooks (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            'default_branch': {
                'type': 'string',
                'description': 'The default branch name',
            },
            'autoclose_referenced_issues': {
                'type': 'boolean',
                'description': 'Set whether auto-closing referenced issues on default branch',
            },
            'issue_branch_template': {
                'type': 'string',
                'description': 'Template used to suggest names for branches created from issues.',
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            'mirror': {
                'type': 'boolean',
                'description': 'Enables pull mirroring in a project',
            },
            'import_url': {
                'type': 'string',
                'description': 'URL to import repository from',
            },
            'mirror_user_id': {
                'type': 'integer',
                'description': 'User responsible for all the activity surrounding a pull mirror event',
            },
            'mirror_overwrites_diverged_branches': {
                'type': 'boolean',
                'description': 'Pull mirror overwrites diverged branches',
            },
            'mirror_trigger_builds': {
                'type': 'boolean',
                'description': 'Pull mirroring triggers builds',
            },
            'only_mirror_protected_branches': {
                'type': 'boolean',
                'description': 'Only mirror protected branches',
            },
            # From https://docs.gitlab.com/ee/api/protected_branches.html#protect-repository-branches
            'protected_branches': {
                'type': 'object',
                'description': 'Protected branches',
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'merge_access_level': {
                            'type': 'string',
                            'description': 'Access levels allowed to merge.',
                            'enum': ['noone', 'developer', 'maintainer', 'admin'],
                        },
                        'allowed_to_merge': {
                            'type': 'array',
                            'description': '',
                            'items': {
                                'oneOf': [
                                    {
                                        'type': 'object',
                                        'description': 'Role',
                                        'properties': {
                                            'role': {
                                                'type': 'string',
                                                'description': 'Role name',
                                                'enum': ['noone', 'developer', 'maintainer', 'admin'],
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'User',
                                        'properties': {
                                            'user': {
                                                'type': 'string',
                                                'description': 'User name',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'Group',
                                        'properties': {
                                            'group': {
                                                'type': 'string',
                                                'description': 'Group full path',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                ],
                            },
                        },
                        'push_access_level': {
                            'type': 'string',
                            'description': 'Access levels allowed to push.',
                            'enum': ['noone', 'developer', 'maintainer', 'admin'],
                        },
                        'allowed_to_push': {
                            'type': 'array',
                            'description': '',
                            'items': {
                                'oneOf': [
                                    {
                                        'type': 'object',
                                        'description': 'Role',
                                        'properties': {
                                            'role': {
                                                'type': 'string',
                                                'description': 'Role name',
                                                'enum': ['noone', 'developer', 'maintainer', 'admin'],
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'User',
                                        'properties': {
                                            'user': {
                                                'type': 'string',
                                                'description': 'User name',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'Group',
                                        'properties': {
                                            'group': {
                                                'type': 'string',
                                                'description': 'Group full path',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'Deploy Key',
                                        'properties': {
                                            'deploy_key': {
                                                'type': 'string',
                                                'description': 'Deploy key Title',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                ],
                            },
                        },
                        'allow_force_push': {
                            'type': 'boolean',
                            'description': 'When enabled, members who can push to this branch can also force push.',
                        },
                        'code_owner_approval_required': {
                            'type': 'boolean',
                            'description': ('Prevent pushes to this branch '
                                            'if it matches an item in the CODEOWNERS file.'),
                        },
                        'allowed_to_unprotect': {
                            'type': 'array',
                            'description': '',
                            'items': {
                                'oneOf': [
                                    {
                                        'type': 'object',
                                        'description': 'Role',
                                        'properties': {
                                            'role': {
                                                'type': 'string',
                                                'description': 'Role name',
                                                'enum': ['developer', 'maintainer', 'admin'],
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'User',
                                        'properties': {
                                            'user': {
                                                'type': 'string',
                                                'description': 'User name',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'description': 'Group',
                                        'properties': {
                                            'group': {
                                                'type': 'string',
                                                'description': 'Group full path',
                                            },
                                        },
                                        'additionalProperties': False,
                                    },
                                ],
                            },
                        },
                    },
                },
                '_example': ('\n'
                             '    main:\n'
                             '      allowed_to_merge::\n'
                             '        - role: developer  # one of noone, developer, maintainer, admin\n'
                             '        - user: my_username  # EE only\n'
                             '        - group: my_group  # EE only\n'
                             '      allowed_to_push::\n'
                             '        - role: noone  # one of noone, developer, maintainer, admin\n'
                             '        - user: my_username  # EE only\n'
                             '        - group: my_group  # EE only\n'
                             '        - deploy_key: Deploy Key Title  # EE only\n'
                             '      allow_force_push: false\n'
                             '      code_owner_approval_required: false  # EE only\n'
                             '      allowed_to_unprotect:  # EE only\n'
                             '        - role: maintainer  # one of developer, maintainer, admin\n'
                             '        - user: my_username\n'
                             '        - group: my_group\n'
                             '    develop:\n'
                             '      merge_access_level: developer\n'
                             '      push_access_level: developer\n'),
            },
            'unknown_protected_branches': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown protected branches (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/protected_tags.html#protect-repository-tags
            'protected_tags': {
                'type': 'object',
                'description': 'Protected tags',
                'additionalProperties': {
                    'type': 'string',
                    'description': 'Access levels allowed to create (defaults: maintainer access level)',
                    'enum': ['noone', 'developer', 'maintainer'],
                },
                '_example': ('\n'
                             '    v*: maintainer # one of noone, developer, maintainer\n'
                             '    *: developer # one of noone, developer, maintainer\n'),
            },
            'unknown_protected_tags': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown protected tags (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            'merge_method': {
                'type': 'string',
                'description': 'Set the merge method used',
                'enum': ['merge', 'rebase_merge', 'ff'],
            },
            'merge_pipelines_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable merged results pipelines.',
            },
            'merge_trains_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable merge trains.',
            },
            'resolve_outdated_diff_discussions': {
                'type': 'boolean',
                'description': 'Automatically resolve merge request diffs discussions on lines changed with a push',
            },
            'printing_merge_request_link_enabled': {
                'type': 'boolean',
                'description': 'Show link to create/view merge request when pushing from the command line',
            },
            'remove_source_branch_after_merge': {
                'type': 'boolean',
                'description': 'Enable Delete source branch option by default for all new merge requests',
            },
            'squash_option': {
                'type': 'string',
                'description': 'Squash option.',
                'enum': ['never', 'always', 'default_on', 'default_off'],
            },
            'only_allow_merge_if_pipeline_succeeds': {
                'type': 'boolean',
                'description': 'Set whether merge requests can only be merged with successful jobs',
            },
            'allow_merge_on_skipped_pipeline': {
                'type': 'boolean',
                'description': 'Set whether or not merge requests can be merged with skipped jobs',
            },
            'only_allow_merge_if_all_discussions_are_resolved': {
                'type': 'boolean',
                'description': 'Set whether merge requests can only be merged when all the discussions are resolved',
            },
            'only_allow_merge_if_all_status_checks_passed': {
                'type': 'boolean',
                'description': ('Indicates that merges of merge requests'
                                'should be blocked unless all status checks have passed.'),
            },
            'suggestion_commit_message': {
                'type': 'string',
                'description': 'The commit message used to apply merge request suggestions',
            },
            'merge_commit_template': {
                'type': 'string',
                'description': 'Template used to create merge commit message in merge requests.',
            },
            'squash_commit_template': {
                'type': 'string',
                'description': 'Template used to create squash commit message in merge requests.',
            },
            'merge_requests_template': {
                'type': 'string',
                'description': 'Default description for merge requests.',
            },
            'approvals_before_merge': {
                'type': 'integer',
                'description': 'How many approvers should approve merge request by default',
                'multipleOf': 1,
                'minimum': 0,
            },

            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            'public_jobs': {
                'type': 'boolean',
                'description': 'If true, jobs can be viewed by non-project members.',
            },
            'auto_cancel_pending_pipelines': {
                'type': 'string',
                'description': 'Auto-cancel pending pipelines',
                'enum': ['enabled', 'disabled'],
            },
            'ci_forward_deployment_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable prevent outdated deployment jobs.',
            },
            'ci_forward_deployment_rollback_allowed': {
                'type': 'boolean',
                'description': 'Enable or disable allow job retries for rollback deployments.',
            },
            'ci_separated_caches': {
                'type': 'boolean',
                'description': 'Set whether or not caches should be separated by branch protection status.',
            },
            'ci_restrict_pipeline_cancellation_role': {
                'type': 'string',
                'description': 'Set the role required to cancel a pipeline or job.',
                'enum': ['developer', 'maintainer', 'no_one'],
            },
            'ci_config_path': {
                'type': 'string',
                'description': 'The path to CI config file',
                '_example': 'debian/salsa-ci.yml',
            },
            'build_git_strategy': {
                'type': 'string',
                'description': 'The Git strategy',
                'enum': ['fetch', 'clone'],
            },
            'ci_default_git_depth': {
                'type': 'integer',
                'description': 'Default number of revisions for shallow cloning',
            },
            'build_timeout': {
                'type': 'integer',
                'description': 'The maximum amount of time in minutes that a job is able run (in seconds)',
            },
            'ci_allow_fork_pipelines_to_run_in_parent_project': {
                'type': 'boolean',
                'description': ('Enable or disable running pipelines in the parent project '
                                'for merge requests from forks.'),
            },
            'auto_devops_enabled': {
                'type': 'boolean',
                'description': 'Enable Auto DevOps for this project',
            },
            'auto_devops_deploy_strategy': {
                'type': 'string',
                'description': 'Auto Deploy strategy',
                'enum': ['continuous', 'manual', 'timed_incremental'],
            },
            'allow_pipeline_trigger_approve_deployment': {
                'type': 'boolean',
                'description': 'Set whether or not a pipeline triggerer is allowed to approve deployments.',
            },
            'shared_runners_enabled': {
                'type': 'boolean',
                'description': 'Enable shared runners for this project.',
            },
            'group_runners_enabled': {
                'type': 'boolean',
                'description': 'Enable group runners for this project.',
            },
            'keep_latest_artifact': {
                'type': 'boolean',
                'description': 'Disable or enable the ability to keep the latest artifact for this project.',
            },
            # From https://docs.gitlab.com/ee/api/project_level_variables.html#create-variable
            'variables': {
                'type': 'array',
                'description': "The list of project's variables",
                'items': {
                    'type': 'object',
                    'properties': {
                        'key': {
                            'type': 'string',
                            'description': 'The key of a variable.',
                            'pattern': '[a-zA-Z0-9_]+',
                            'maxLength': 255,
                        },
                        'value': {
                            'type': 'string',
                            'description': 'The value of a variable.',
                        },
                        'description': {
                            'type': 'string',
                            'description': 'The description of the variable.',
                        },
                        'variable_type': {
                            'type': 'string',
                            'description': 'The type of a variable. Available types are: env_var (default) and file.',
                            'enum': ['env_var', 'file'],
                        },
                        'protected': {
                            'type': 'boolean',
                            'description': 'Whether the variable is protected.',
                        },
                        'masked': {
                            'type': 'boolean',
                            'description': 'Whether the variable is masked.',
                        },
                        'raw': {
                            'type': 'boolean',
                            'description': 'Whether the variable is treated as a raw string.',
                        },
                        'environment_scope': {  # Premium+/Silver+
                            'type': 'string',
                            'description': 'The environment_scope of the variable.',
                        },
                    },
                    'required': ['key'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - key: DAST_DISABLED\n'
                             "      value: '1'\n"
                             '      description: Disabled SAST\n'
                             '      masked: false\n'
                             '      protected: false\n'
                             '      raw: false  # Expand variables\n'
                             "      environment_scope: '*'\n"
                             '      variable_type: env_var\n'),
            },
            'unknown_variables': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown variables (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            # container_expiration_policy_attributes
            'container_expiration_policy': {
                'type': 'object',
                'description': 'Update the image cleanup policy for this project',
                'properties': {
                    'enabled': {
                        'type': 'boolean',
                    },
                    'cadence': {
                        'type': 'string',
                    },
                    'keep_n': {
                        'type': 'integer',
                    },
                    'name_regex_keep': {
                        'type': 'string',
                    },
                    'older_than': {
                        'type': 'string',
                    },
                    'name_regex_delete': {
                        'type': 'string',
                    },
                },
                'required': ['enabled'],
                'additionalProperties': False,
                '_example': ('\n'
                             '    enabled: true\n'
                             '    cadence: 7d # 1d, 7d, 14d, 1month, 3month\n'
                             '    keep_n: 10 # 1, 5, 10, 25, 50, 100\n'
                             "    name_regex_keep: '.*main|.*release|release-.*|main-.*'\n"
                             '    older_than: 90d\n'
                             "    name_regex_delete: '.*'\n"),
            },
            # GitLabracadabra
            'mirrors': {
                'type': 'array',
                'description': "The list of project's mirrors",
                'items': {
                    'type': 'object',
                    'properties': {
                        'url': {
                            'type': 'string',
                            'description': 'Repository URL',
                        },
                        'auth_id': {
                            'type': 'string',
                            'description': 'Section from .python-gitlab.cfg for authentication',
                        },
                        'direction': {
                            'type': 'string',
                            'description': 'Mirror direction',
                            'enum': ['pull', 'push'],
                        },
                        'skip_ci': {
                            'type': 'boolean',
                            'description': 'Skip CI during push',
                        },
                        'push_options': {
                            'type': 'array',
                            'description': 'Default push options',
                            'items': {
                                'type': 'string',
                            },
                        },
                        'branches': {
                            'type': 'array',
                            'description': 'The branches mapping',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'from': {
                                        'type': 'string',
                                        'description': 'Source name or regular expression',
                                    },
                                    'to': {
                                        'type': 'string',
                                        'description': 'Destination name or regular expression template',
                                    },
                                    'push_options': {
                                        'type': 'array',
                                        'description': 'Push options',
                                        'items': {
                                            'type': 'string',
                                        },
                                    },
                                },
                                'required': ['from'],
                                'additionalProperties': False,
                            },
                            'uniqueItems': True,
                        },
                        'tags': {
                            'type': 'array',
                            'description': 'The tags mapping',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'from': {
                                        'type': 'string',
                                        'description': 'Source name or regular expression',
                                    },
                                    'to': {
                                        'type': 'string',
                                        'description': 'Destination name or regular expression template',
                                    },
                                    'push_options': {
                                        'type': 'array',
                                        'description': 'Push options',
                                        'items': {
                                            'type': 'string',
                                        },
                                    },
                                },
                                'required': ['from'],
                                'additionalProperties': False,
                            },
                            'uniqueItems': True,
                        },
                    },
                    'required': ['url'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - url: https://gitlab.com/gitlabracadabra/gitlabracadabra.git\n'
                             '      # auth_id: gitlab # Section from .python-gitlab.cfg for authentication\n'
                             '      direction: pull # one of pull, push ; only first pull mirror is processed\n'
                             '      push_options: [ci.skip]\n'
                             '      branches: # if you omit this parameter, all branches are mirrored\n'
                             "        - from: '/wip-.*/'\n"
                             "          to: '' # This will skip those branches\n"
                             '        - from: main\n'
                             '          # to: main # implicitly equal to source branch\n'
                             '          # push_options: [] # inherited by default\n'
                             '        # Using regexps\n'
                             "        - from: '/(.*)/'\n"
                             "          to: 'upstream/\\1'\n"
                             '      tags: # if you omit this parameter, all tags are mirrored\n'
                             "        - from: '/v(.*)/i'\n"
                             "          to: 'upstream-\\1'\n"
                             '          # push_options: [] # inherited by default\n'
                             '  builds_access_level: disabled # If you want to prevent triggering pipelines on push'),
                '_doc_link': 'mirrors.md',
            },
            'package_mirrors': {
                'type': 'array',
                'description': 'Package image mirrors',
                'items': {
                    'oneOf': [
                        {
                            'type': 'object',
                            'description': 'Raw source',
                            'properties': {
                                'enabled': {
                                    'type': 'boolean',
                                },
                                'raw': {
                                    'type': 'object',
                                    'properties': {
                                        'default_url': {
                                            'type': 'string',
                                        },
                                        'default_package_name': {
                                            'type': 'string',
                                        },
                                        'default_package_version': {
                                            'type': 'string',
                                        },
                                        'package_files': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'url': {
                                                        'type': 'string',
                                                    },
                                                    'package_name': {
                                                        'type': 'string',
                                                    },
                                                    'package_version': {
                                                        'type': 'string',
                                                    },
                                                    'file_name': {
                                                        'type': 'string',
                                                    },
                                                },
                                                'additionalProperties': False,
                                            },
                                        },
                                    },
                                    'required': ['default_url'],
                                    'additionalProperties': False,
                                },
                            },
                            'additionalProperties': False,
                        },
                        {
                            'type': 'object',
                            'description': 'Github source',
                            'properties': {
                                'enabled': {
                                    'type': 'boolean',
                                },
                                'github': {
                                    'type': 'object',
                                    'properties': {
                                        'full_name': {
                                            'type': 'string',
                                        },
                                        'package_name': {
                                            'type': 'string',
                                        },
                                        'tags': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string',
                                            },
                                        },
                                        'semver': {
                                            'type': 'string',
                                        },
                                        'latest_release': {
                                            'type': 'boolean',
                                        },
                                        'tarball': {
                                            'type': 'boolean',
                                        },
                                        'zipball': {
                                            'type': 'boolean',
                                        },
                                        'assets': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string',
                                            },
                                        },
                                    },
                                    'required': ['full_name'],
                                    'additionalProperties': False,
                                },
                            },
                            'additionalProperties': False,
                        },
                        {
                            'type': 'object',
                            'description': 'Helm source',
                            'properties': {
                                'enabled': {
                                    'type': 'boolean',
                                },
                                'helm': {
                                    'type': 'object',
                                    'properties': {
                                        'repo_url': {
                                            'type': 'string',
                                        },
                                        'package_name': {
                                            'type': 'string',
                                        },
                                        'versions': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string',
                                            },
                                        },
                                        'semver': {
                                            'type': 'string',
                                        },
                                        'limit': {
                                            'type': 'integer',
                                        },
                                        'channel': {
                                            'type': 'string',
                                        },
                                    },
                                    'required': ['repo_url', 'package_name'],
                                    'additionalProperties': False,
                                },
                            },
                            'additionalProperties': False,
                        },
                        {
                            'type': 'object',
                            'description': 'PyPI source',
                            'properties': {
                                'enabled': {
                                    'type': 'boolean',
                                },
                                'pypi': {
                                    'type': 'object',
                                    'properties': {
                                        'index_url': {
                                            'type': 'string',
                                        },
                                        'requirements': {
                                            'oneOf': [
                                                {
                                                    'type': 'string',
                                                },
                                                {
                                                    'type': 'array',
                                                    'items': {
                                                        'type': 'string',
                                                    },
                                                },
                                            ],
                                        },
                                    },
                                    'required': ['requirements'],
                                    'additionalProperties': False,
                                },
                            },
                            'additionalProperties': False,
                        },
                    ],
                },
                '_example': ('\n'
                             '    - raw:\n'
                             '        default_url: https://download.docker.com/linux/debian/gpg\n'
                             '        default_package_name: docker\n'
                             "        default_package_version: '0'\n"),
                '_doc_link': 'package_mirrors.md',
            },
            'image_mirrors': {
                'type': 'array',
                'description': 'Container image mirrors',
                'items': {
                    'type': 'object',
                    'properties': {
                        'enabled': {
                            'type': 'boolean',
                        },
                        'from': {
                            'oneOf': [
                                {
                                    'type': 'string',
                                    'description': 'The source image',
                                    'pattern': '.+',
                                },
                                {
                                    'type': 'object',
                                    'properties': {
                                        'base': {
                                            'type': 'string',
                                        },
                                        'repositories': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string',
                                            },
                                        },
                                        'tags': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string',
                                            },
                                        },
                                    },
                                    'required': ['repositories'],
                                    'additionalProperties': False,
                                },
                            ],
                        },
                        'to': {
                            'oneOf': [
                                {
                                    'type': 'string',
                                    'description': 'The destination image',
                                },
                                {
                                    'type': 'object',
                                    'properties': {
                                        'base': {
                                            'type': 'string',
                                        },
                                        'repository': {
                                            'type': 'string',
                                        },
                                        'tag': {
                                            'type': 'string',
                                        },
                                    },
                                    'additionalProperties': False,
                                },
                            ],
                        },
                        'semver': {
                            'type': 'string',
                            'description': 'Version specification as an NPM range',
                        },
                    },
                    'required': ['from'],
                    'additionalProperties': False,
                },
                '_example': ('\n'
                             '    # Mirror debian:bullseye\n'
                             '    # ... to registry.example.org/mygroup/myproject/library/debian:bullseye:\n'
                             "    - from: 'debian:bullseye'\n"
                             '    # Overriding destination:\n'
                             "    - from: 'quay.org/coreos/etcd:v3.4.1'\n"
                             "      to: 'etcd:v3.4.1' # Default would be coreos/etcd:v3.4.1\n"),
                '_doc_link': 'image_mirrors.md',
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            # Deprecated
            'build_coverage_regex': {
                'type': 'string',
                'description': '(Removed) Test coverage parsing.',
            },
            'container_registry_enabled': {
                'type': 'boolean',
                'description': ('(Deprecated) Enable container registry for this project. '
                                'Use container_registry_access_level instead.'),
            },
            'emails_disabled': {
                'type': 'boolean',
                'description': '(Deprecated) Disable email notifications. Use emails_enabled instead.',
            },
            'issues_enabled': {
                'type': 'boolean',
                'description': '(Deprecated) Enable issues for this project. Use issues_access_level instead.',
            },
            'jobs_enabled': {
                'type': 'boolean',
                'description': '(Deprecated) Enable jobs for this project. Use builds_access_level instead.',
            },
            'merge_requests_enabled': {
                'type': 'boolean',
                'description': ('(Deprecated) Enable merge requests for this project. '
                                'Use merge_requests_access_level instead.'),
            },
            'public_builds': {
                'type': 'boolean',
                'description': ('(Deprecated) If true, jobs can be viewed by non-project members. '
                                'Use public_jobs instead.'),
            },
            'snippets_enabled': {
                'type': 'boolean',
                'description': '(Deprecated) Enable snippets for this project. Use snippets_access_level instead.',
            },
            'tag_list': {
                'type': 'array',
                'description': ('(Deprecated in GitLab 14.0) The list of tags for a project; put array of tags, '
                                'that should be finally assigned to a project. Use topics instead.'),
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
                '_example': '[GitLab, API, YAML]',
            },
            'wiki_enabled': {
                'type': 'boolean',
                'description': '(Deprecated) Enable wiki for this project. Use wiki_access_level instead.',
            },
            # Below are undocumented settings
            'repository_storage': {
                'type': 'string',
                'description': 'Which storage shard the repository is on. Available only to admins',
            },
            'external_authorization_classification_label': {
                'type': 'string',
                'description': 'The classification label for the project',
            },
        },
        'additionalProperties': False,
    }

    IGNORED_PARAMS = ['initialize_with_readme',
                      'repository_object_format',
                      'unknown_boards',
                      'unknown_board_lists',
                      'unknown_groups',
                      'unknown_labels',
                      'unknown_members',
                      'unknown_milestones',
                      'unknown_pipeline_schedules',
                      'unknown_pipeline_schedule_variables',
                      'unknown_protected_branches',
                      'unknown_protected_tags',
                      'unknown_variables',
                      'unknown_webhooks']

    CREATE_KEY = 'name'
    CREATE_PARAMS = ['initialize_with_readme', 'repository_object_format']

    def _get_current_branches(self):
        if not hasattr(self, '_current_branches'):
            try:
                self._current_branches = [branch.name for branch in self._obj.branches.list(all=True)]
            except GitlabListError as err:
                if err.response_code != 403:  # repository_enabled=false?
                    pass
                self._current_branches = None
        return self._current_branches

    """"_process_archived()

    Process the archived param.
    """
    def _process_archived(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'archived'  # noqa: S101
        assert not skip_save  # noqa: S101

        current_value = getattr(self._obj, param_name)
        if current_value != param_value:
            if dry_run:
                logger.info('[%s] NOT Changing param %s: %s -> %s (dry-run)',
                            self._name, param_name, current_value, param_value)
                setattr(self._obj, param_name, param_value)
            else:
                logger.info('[%s] Changing param %s: %s -> %s',
                            self._name, param_name, current_value, param_value)
                if param_value:
                    self._obj.archive()
                else:
                    self._obj.unarchive()

    """"_process_branches()

    Process the branches param.
    """
    def _process_branches(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'branches'  # noqa: S101
        assert not skip_save  # noqa: S101
        if 'default_branch' in self._content and self._content['default_branch'] in self._get_current_branches():
            # Create from target default branch if it exists
            ref = self._content['default_branch']
        elif self._obj.default_branch in self._get_current_branches():
            # Create from current default branch otherwise
            ref = self._obj.default_branch
        else:
            ref = None
        for branch_name in param_value:
            if branch_name not in self._get_current_branches():
                if ref is None:
                    logger.info('[%s] NOT Creating branch: %s (no reference)',
                                self._name, branch_name)
                elif dry_run:
                    logger.info('[%s] NOT Creating branch: %s (dry-run)',
                                self._name, branch_name)
                    self._current_branches.append(branch_name)
                else:
                    logger.info('[%s] Creating branch: %s',
                                self._name, branch_name)
                    self._obj.branches.create({
                        'branch': branch_name,
                        'ref': ref,
                    })
                    self._current_branches.append(branch_name)
            if branch_name in self._get_current_branches():
                # Next branch will be created from this ref
                ref = branch_name

    """"_process_protected_tags()

    Process the protected_tags param.
    """
    def _process_protected_tags(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'protected_tags'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_protected_tags = self._content.get('unknown_protected_tags', 'warn')
        try:
            current_protected_tags = dict([[protected_tag.name, protected_tag]
                                           for protected_tag in self._obj.protectedtags.list(all=True)])
        except AttributeError:
            logger.error('[%s] Unable to manage protected tags: %s',
                         self._name, 'protected tags requires python-gitlab >= 1.7.0')
            return
        # We first check for already protected tags
        for protected_name, target_config in sorted(param_value.items()):
            target_config = {
                'name': protected_name,
                'create_access_level': access_level_value(target_config),
            }
            if protected_name in current_protected_tags:
                current_protected_tag = current_protected_tags[protected_name]
                current_config = {
                    'name': protected_name,
                    'create_access_level': current_protected_tag.create_access_levels[0]['access_level'],
                }
            else:
                current_config = {}
            if current_config != target_config:
                if dry_run:
                    logger.info('[%s] NOT Changing protected tag %s access level: %s -> %s (dry-run)',
                                self._name, protected_name, current_config, target_config)
                else:
                    logger.info('[%s] Changing protected tag %s access level: %s -> %s',
                                self._name, protected_name, current_config, target_config)
                    if 'name' in current_config:
                        self._obj.protectedtags.delete(protected_name)
                    self._obj.protectedtags.create(target_config)
        # Remaining protected tags
        if unknown_protected_tags not in ['ignore', 'skip']:
            current_protected_tags = sorted(protected_tag.name
                                            for protected_tag in self._obj.protectedtags.list(all=True))
            for protected_name in current_protected_tags:
                if protected_name not in param_value:
                    if unknown_protected_tags in ['delete', 'remove']:
                        if dry_run:
                            logger.info('[%s] NOT Deleting unknown protected tag: %s (dry-run)',
                                        self._name, protected_name)
                        else:
                            logger.info('[%s] Deleting unknown protected tag: %s',
                                        self._name, protected_name)
                            self._obj.protectedtags.delete(protected_name)
                    else:
                        logger.warning('[%s] NOT Deleting unknown protected tag: %s (unknown_protected_tags=%s)',
                                       self._name, protected_name, unknown_protected_tags)

    """"_process_container_expiration_policy()

    Process the container_expiration_policy param.
    """
    def _process_container_expiration_policy(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'container_expiration_policy'  # noqa: S101
        assert not skip_save  # noqa: S101

        current_value = getattr(self._obj, param_name)

        for k, v in sorted(param_value.items()):
            current_v = current_value.get(k, None)
            if v != current_v:
                if dry_run:
                    logger.info('[%s] NOT Changing container expiration policy %s: %s -> %s (dry-run)',
                                self._name, k, current_v, v)
                else:
                    logger.info('[%s] Changing container expiration policy %s: %s -> %s',
                                self._name, k, current_v, v)
                    self._obj.container_expiration_policy_attributes = {k: v}
                    self._obj.save()
