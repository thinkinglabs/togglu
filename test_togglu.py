#!/usr/bin/env python3

import unittest
import togglu

import mountepy

import io
import sys


class TestTogglU(unittest.TestCase):

    def test_workspaces(self):
        actual_output = io.StringIO();
        sys.stdout = actual_output;

        with open('workspaces.json', 'r') as myfile:
            data = myfile.read().replace('\n', '')

        with mountepy.Mountebank() as mb:
            imposter = mb.add_imposter_simple(path='/workspaces', response=data)
            stub_url = 'http://localhost:{}'.format(imposter.port)

            cli = togglu.CLI(['--url', stub_url])
            cli.execute()
            sys.stdout = sys.__stdout__

            expected_output = "1234567:workspace 1\n2345678:workspace 2\n3456789:workspace 3\n\n"
            self.assertEqual(actual_output.getvalue(), expected_output);

if __name__ == '__main__':
    unittest.main()

