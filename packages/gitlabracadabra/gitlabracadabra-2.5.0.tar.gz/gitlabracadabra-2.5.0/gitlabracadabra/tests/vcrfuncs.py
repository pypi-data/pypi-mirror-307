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

import inspect
import os
import re
from base64 import standard_b64decode, standard_b64encode

from vcr import VCR
from vcr.matchers import body


def _gitlabracadabra_func_path_generator(function):
    func_file = inspect.getfile(function)
    method_name = function.__name__  # test_no_create
    instance_name = function.__self__.__class__.__name__  # TestUser
    fixture_name = (re.sub(r'^Test', r'', instance_name) +
                    '_' +
                    re.sub(r'^test_', r'', method_name) +
                    '.yaml')
    return os.path.join(os.path.dirname(func_file),
                        'fixtures',
                        fixture_name,
                        )


def _gitlabracadabra_uri_matcher(r1, r2):
    r1_uri = r1.uri
    r2_uri = r2.uri
    # Workaround 'all=True' in API calls
    # with python-gitlab < 1.8.0
    # See https://github.com/python-gitlab/python-gitlab/pull/701
    if r1_uri.endswith('all=True'):
        r1_uri = r1_uri[0:-9]
    # Ignore host and port
    r1_uri = re.sub('http://[^:/]+(:\\d+)?/', 'http://localhost/', r1_uri)
    r2_uri = re.sub('http://[^:/]+(:\\d+)?/', 'http://localhost/', r2_uri)
    return r1_uri == r2_uri


def _gitlabracadabra_body_matcher(r1, r2):
    if (
        r1.method == 'POST' and
        r1.method == r2.method and
        r1.url == r2.url
    ):
        _, _, r1_boundary = r1.headers.get('Content-Type', '').partition('multipart/form-data; boundary=')
        _, _, r2_boundary = r2.headers.get('Content-Type', '').partition('multipart/form-data; boundary=')
        return (
            r1_boundary and
            r2_boundary and
            r1.body.split(r1_boundary.encode()) == r2.body.split(r2_boundary.encode())
        )
    else:
        return body(r1, r2)


def _gitlabracadabra_headers(headers: dict[str, str]) -> dict[str, str]:
    new_headers: dict[str, str] = {}
    for header_name, header_value in headers.items():
        if header_name == 'Accept':
            if header_value != '*/*':
                header_value = 'boilerplate'
        if header_name == 'Accept-Encoding':
            if header_value == '*':
                header_value = 'gzip, deflate'
        elif header_name == 'Authorization':
            if header_value.startswith('Basic '):
                userpass = standard_b64decode(header_value.removeprefix('Basic ')).split(b':')
                userpass[1] = b'my-pass'
                basic_value = standard_b64encode(b':'.join(userpass)).decode('ascii')
                header_value = f'Basic {basic_value}'
            elif header_value.startswith('Bearer '):
                header_value = 'Bearer some-value'
        elif header_name == 'Content-Length':
            header_value = '42'
        elif header_name == 'Content-Type':
            if header_value.startswith('multipart/form-data; boundary='):
                header_value = 'multipart/form-data; boundary=some-boundary'
        elif header_name == 'PRIVATE-TOKEN':
            header_value = 'MY-TOKEN'
        elif header_name in {'Content-type', 'Cookie', 'User-Agent'}:
            continue
        new_headers[header_name] = header_value
    return new_headers


def _gitlabracadabra_headers_matcher(r1, r2):
    r1_headers = _gitlabracadabra_headers(r1.headers)
    r2_headers = _gitlabracadabra_headers(r2.headers)
    if r1_headers != r2_headers:
        raise AssertionError(f'{r1_headers} != {r2_headers}')
    return r1_headers == r2_headers  # compat


my_vcr = VCR(
    match_on=['method', 'gitlabracadabra_uri', 'body', 'gitlabracadabra_headers'],
    func_path_generator=_gitlabracadabra_func_path_generator,
    record_mode='none',  # change to 'once' or 'new_episodes'
    inject_cassette=True,
    decode_compressed_response=True,
)
my_vcr.register_matcher('gitlabracadabra_uri', _gitlabracadabra_uri_matcher)
my_vcr.register_matcher('gitlabracadabra_body', _gitlabracadabra_body_matcher)
my_vcr.register_matcher('gitlabracadabra_headers', _gitlabracadabra_headers_matcher)
