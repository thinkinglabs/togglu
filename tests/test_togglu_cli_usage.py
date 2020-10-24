
import unittest
import io
import locale
import sys

from .context import togglu
from togglu import togglu

class TestCLI(unittest.TestCase):

    def test_required_subcommand(self):
        actual_output = io.StringIO()
        sys.stderr = actual_output

        try:
            cli = togglu.CLI()
            cli.execute()

        except SystemExit:
            expected_output = \
                'usage: togglu.py [-h] [--toggl-url TOGGL_URL] [--reports-url REPORTS_URL]' \
                ' {workspaces,timesheet} ...\n' \
                'togglu.py: error: the following arguments are required: subcommand\n'

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
                'usage: togglu.py timesheet [-h] --workspace-id WORKSPACE_ID [--since SINCE]' \
                ' [--until UNTIL] [--client-id CLIENT_ID]' \
                ' [--tag-id TAG_ID]\n' \
                'togglu.py timesheet: error: the following arguments are required: --workspace-id\n'
                
            self.assertEqual(actual_output.getvalue(), expected_output)

        finally:
            sys.stderr = sys.__stderr__
