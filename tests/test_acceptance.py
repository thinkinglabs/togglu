#!/usr/bin/env python3

import unittest
import os
import io
import locale
import sys
import configparser as ConfigParser

from .helpers.http import mock_http_server
from .helpers.http import WorkspacesRequestHandler, DetailedReportPaginationRequestHandler

from .context import togglu
from togglu import togglu


class TestTogglU(unittest.TestCase):

    cfg_file = '/tmp/togglrc'

    def setUp(self):
        # TODO: replace by Config.create_empty_config()
        cfg = ConfigParser.RawConfigParser()
        cfg.add_section('auth')
        cfg.set('auth', 'api_token', 'your_api_token')
        with open(os.path.expanduser(self.cfg_file), 'w') as cfgfile:
            cfg.write(cfgfile)

    def tearDown(self):
        os.remove(os.path.expanduser(self.cfg_file))

    def test_workspaces(self):
        mock_server_port = mock_http_server(WorkspacesRequestHandler)

        stub_url = f'http://localhost:{mock_server_port}'

        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            cli = togglu.CLI(['--config', self.cfg_file, '--toggl-url', stub_url, 'workspaces'])
            cli.execute()

            expected_output = "1234567:workspace 1\n2345678:workspace 2\n3456789:workspace 3\n"
            self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__

    def test_timesheet(self):
        mock_server_port = mock_http_server(DetailedReportPaginationRequestHandler)

        stub_url = f'http://localhost:{mock_server_port}'

        self.maxDiff = None
        default_time_locale = locale.getlocale(locale.LC_TIME)[0]

        try:
            locale.setlocale(locale.LC_TIME, 'fr_BE.UTF-8')
            actual_output = io.StringIO()
            sys.stdout = actual_output

            cli = togglu.CLI(
                ['--config', self.cfg_file, '--reports-url', stub_url, 'timesheet', '--workspace-id', '123'])
            cli.execute()

            expected_output = \
                '06.12.2018 | Kaloo                          |       1.90\n' \
                '05.12.2018 | VooFix                         |       8.14\n' \
                '23.11.2018 | VooFix                         |       8.54\n' \
                '11.11.2018 | Wikimba                        |       0.11\n' \
                '11.11.2018 | Kwimbee                        |       0.05\n' \
                'total hours: 18.74\n' \
                'days worked: 4.00\n'
            self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__
            locale.setlocale(locale.LC_TIME, default_time_locale)


if __name__ == '__main__':
    unittest.main()
