#!/usr/bin/env python3

import unittest
import togglu

import io
import sys

class TestTogglU(unittest.TestCase):

    def test_workspaces(self):
        actual_output = io.StringIO();
        sys.stdout = actual_output;
        cli = togglu.CLI(['workspaces'])
        cli.execute()
        sys.stdout = sys.__stdout__

        expected_output = "509982:Way of Thinking\n2875607:Private\n2875631:Mamie\n\n"
        self.assertEqual(actual_output.getvalue(), expected_output);

if __name__ == '__main__':
    unittest.main()

