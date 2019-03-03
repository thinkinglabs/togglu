#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import io
import locale
import sys
import os

import mountepy
import port_for

from .context import togglu
from togglu import togglu

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestCLI(unittest.TestCase):

    def test_required_subcommand(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI()
            cli.execute()

        except SystemExit:
            expected_output = \
                "usage: togglu.py [-h] [--toggl-url TOGGL_URL] [--reports-url REPORTS_URL]\n" \
                "                 {workspaces,timesheet} ...\n" \
                "togglu.py: error: the following arguments are required: subcommand\n"

            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__

    def test_required_arguments_for_timesheet(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI(['timesheet'])
            cli.execute()

        except SystemExit:
            expected_output = \
                'usage: togglu.py timesheet [-h] --workspace-id WORKSPACE_ID [--since SINCE]\n' \
                '                           [--until UNTIL] [--client-id CLIENT_ID]\n' \
                '                           [--tag-id TAG_ID]\n' \
                'togglu.py timesheet: error: the following arguments are required: --workspace-id\n'
                
            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__

class TestTogglU(unittest.TestCase):

    def test_workspaces(self):
        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            with open(os.path.join(THIS_DIR, os.pardir,'tests/workspaces.json'), 'r') as myfile:
                data = myfile.read().replace('\n', '')

            with mountepy.Mountebank() as mb:
                imposter = mb.add_imposter_simple(path='/workspaces', response=data)
                stub_url = 'http://localhost:{}'.format(imposter.port)

                cli = togglu.CLI(['--toggl-url', stub_url, 'workspaces'])
                cli.execute()

                expected_output = "1234567:workspace 1\n2345678:workspace 2\n3456789:workspace 3\n\n"
                self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__

    def test_timesheet(self):
        self.maxDiff = None
        default_time_locale = locale.getlocale(locale.LC_TIME)[0]

        try:
            locale.setlocale(locale.LC_TIME, 'fr_BE')
            actual_output = io.StringIO()
            sys.stdout = actual_output

            with open(os.path.join(THIS_DIR, os.pardir,'tests/detailed_report_page1.json'), 'r') as myfile:
                data1 = myfile.read().replace('\n', '')
            with open(os.path.join(THIS_DIR, os.pardir,'tests/detailed_report_page2.json'), 'r') as myfile:
                data2 = myfile.read().replace('\n', '')
            with open(os.path.join(THIS_DIR, os.pardir,'tests/detailed_report_page3.json'), 'r') as myfile:
                data3 = myfile.read().replace('\n', '')

            with mountepy.Mountebank() as mb:
                imposter = mb.add_imposter({
                    'protocol': 'http',
                    'port': port_for.select_random(),
                    'stubs': [
                        {
                            'predicates': [
                                {
                                    'equals': {
                                        'method': 'GET',
                                        'path': '/details',
                                        'query': { 'page': '1'}
                                    }
                                }
                            ],
                            'responses': [
                                {
                                    'is': {
                                        'statusCode': 200,
                                        'headers': {'Content-Type': 'application/json'},
                                        'body': data1
                                    }
                                }
                            ]
                        },
                        {
                            'predicates': [
                                {
                                    'equals': {
                                            'method': 'GET',
                                            'path': '/details',
                                            'query': { 'page': '2'}
                                    }
                                }
                            ],
                            'responses': [
                                {
                                    'is': {
                                        'statusCode': 200,
                                        'headers': {'Content-Type': 'application/json'},
                                        'body': data2
                                    }
                                }
                            ]
                        },
                        {
                            'predicates': [
                                {
                                    'equals': {
                                        'method': 'GET',
                                        'path': '/details',
                                            'query': { 'page': '3'}
                                    }
                                }
                            ],
                            'responses': [
                                {
                                    'is': {
                                        'statusCode': 200,
                                        'headers': {'Content-Type': 'application/json'},
                                        'body': data3
                                    }
                                }
                            ]
                        }
                    ]
                })

                stub_url = 'http://localhost:{}'.format(imposter.port)

                cli = togglu.CLI(['--reports-url', stub_url, 'timesheet', '--workspace-id', '123'])
                cli.execute()
                
                expected_output = \
                    '06.12.2018 | Kaloo                          |       1.90\n' \
                    '05.12.2018 | VooFix                         |       8.14\n' \
                    '23.11.2018 | VooFix                         |       8.54\n' \
                    '11.11.2018 | Wikimba                        |       0.11\n' \
                    '11.11.2018 | Kwimbee                        |       0.05\n' \
                    'days worked: 4\n'
                self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__
            locale.setlocale(locale.LC_TIME, default_time_locale)

if __name__ == '__main__':
    unittest.main()
