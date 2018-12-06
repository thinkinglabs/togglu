#!/usr/bin/env python3

import unittest
import togglu

import mountepy

import io
import sys

import argparse


class TestCLI(unittest.TestCase):

    def test_workspaces_required(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI()
        except BaseException as err:

            expected_output = 'usage: togglu.py [-h] [--toggl-url TOGGL_URL] [--reports-url REPORTS_URL]\n                 --workspaces\ntogglu.py: error: the following arguments are required: --workspaces\n'
            self.assertEqual(actual_output.getvalue(), expected_output)

            pass
        finally:
            sys.stdout = sys.__stderr__


class TestTogglU(unittest.TestCase):

    def test_workspaces(self):
        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            with open('workspaces.json', 'r') as myfile:
                data = myfile.read().replace('\n', '')

            with mountepy.Mountebank() as mb:
                imposter = mb.add_imposter_simple(path='/workspaces', response=data)
                stub_url = 'http://localhost:{}'.format(imposter.port)

                cli = togglu.CLI(['--toggl-url', stub_url, '--workspaces'])
                cli.execute()

                expected_output = "1234567:workspace 1\n2345678:workspace 2\n3456789:workspace 3\n\n"
                self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__



if __name__ == '__main__':
    unittest.main()

