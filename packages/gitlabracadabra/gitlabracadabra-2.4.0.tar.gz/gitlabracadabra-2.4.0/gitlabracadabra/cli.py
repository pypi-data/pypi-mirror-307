#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
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

from __future__ import annotations, print_function

import logging
import sys
from argparse import ArgumentParser
from typing import Sequence

import gitlabracadabra
import gitlabracadabra.parser
from gitlabracadabra.gitlab.connections import GitlabConnections


logger = logging.getLogger(__name__)


def _get_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description='GitLabracadabra')
    parser.add_argument('--version', help='Display the version.',
                        action='store_true')
    parser.add_argument('-v', '--verbose', '--fancy',
                        help='Verbose mode',
                        action='store_true')
    parser.add_argument('-d', '--debug',
                        help='Debug mode (display HTTP requests)',
                        action='store_true')
    parser.add_argument('--logging-format',
                        help='Logging format',
                        choices=['short', 'long'],
                        default='short')
    parser.add_argument('-c', '--config-file', action='append',
                        help=('Configuration file to use. Can be used '
                              'multiple times.'))
    parser.add_argument('-g', '--gitlab',
                        help=('Which configuration section should '
                              'be used. If not defined, the default selection '
                              'will be used.'),
                        required=False)
    parser.add_argument('--dry-run',
                        help='Dry run',
                        action='store_true')
    parser.add_argument('--fail-on-errors',
                        help='Fail on errors',
                        action='store_true')
    parser.add_argument('--fail-on-warnings',
                        help='Fail on warnings',
                        action='store_true')
    parser.add_argument('--doc-markdown',
                        help=('Output the help for the given type (project, '
                              'group, user, application_settings) as '
                              'Markdown.'))
    parser.add_argument('action_files',
                        help='Action file. Can be used multiple times.',
                        metavar='ACTIONFILE.yml',
                        nargs='*',
                        default=['gitlabracadabra.yml'])

    return parser


class ExitCodeHandler(logging.Handler):
    def __init__(self) -> None:
        logging.Handler.__init__(self)
        self._max_levelno: int = logging.NOTSET

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno > self._max_levelno:
            self._max_levelno = record.levelno

    @property
    def max_levelno(self) -> int:
        return self._max_levelno


def main(args: Sequence[str] | None = None) -> None:
    argument_parser = _get_argument_parser()

    namespace = argument_parser.parse_args(args)

    if namespace.version:
        print(gitlabracadabra.__version__)
        sys.exit(0)

    config_files = namespace.config_file
    gitlab_id = namespace.gitlab

    if namespace.logging_format == 'long':
        logging_format = '%(asctime)s [%(process)d] %(levelname)-8.8s %(name)s: %(message)s'
    else:
        logging_format = '%(levelname)-8.8s %(message)s'
    log_level = logging.WARNING
    if namespace.verbose:
        log_level = logging.INFO
    if namespace.debug:
        log_level = logging.DEBUG
    exit_code_handler = ExitCodeHandler()
    logging.basicConfig(
        format=logging_format,
        level=log_level,
    )
    logging.root.addHandler(exit_code_handler)

    if namespace.doc_markdown:
        cls = gitlabracadabra.parser.GitlabracadabraParser.get_class_for(namespace.doc_markdown)
        print(cls.doc_markdown())
        sys.exit(0)

    try:
        GitlabConnections().load(gitlab_id, config_files, namespace.debug)
    except Exception as e:  # noqa: B902
        logger.error(str(e))  # noqa: G200
        sys.exit(1)

    # First pass: Load data and preflight checks
    objects = {}
    has_errors = False
    for action_file in namespace.action_files:
        if action_file.endswith('.yml') or action_file.endswith('.yaml'):
            parser = gitlabracadabra.parser.GitlabracadabraParser.from_yaml_file(action_file)
        else:
            logger.error('Unhandled file: %s', action_file)
            has_errors = True
            continue
        logger.debug('Parsing file: %s', action_file)
        objects[action_file] = parser.objects()
        for k, v in sorted(objects[action_file].items()):
            if len(v.errors()) > 0:
                for error in v.errors():
                    logger.error('Error in %s (%s %s): %s', action_file, v._type_name(), k, str(error))
                has_errors = True

    if has_errors:
        logger.error('Preflight checks errors. Exiting')
        sys.exit(1)

    # Second pass:
    for action_file in namespace.action_files:
        for _name, obj in sorted(objects[action_file].items()):
            obj.process(namespace.dry_run)

    fails_on = logging.CRITICAL
    if namespace.fail_on_errors:
        fails_on = logging.ERROR
    if namespace.fail_on_warnings:
        fails_on = logging.WARNING
    if exit_code_handler.max_levelno >= fails_on:
        sys.exit(1)


if __name__ == '__main__':
    main()
