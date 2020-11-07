
import unittest
from unittest.mock import patch

import sys
import io

from .context import togglu  # noqa: F401
from togglu.workspaces_console_renderer import WorkspaceConsoleRenderer
from togglu.workspace import Workspace


class WorkspaceConsoleRendererTestCase(unittest.TestCase):

    @patch('togglu.toggl_repository.TogglRepository')
    def test_render(self, toggl_repository):
        toggl_repository.workspaces.return_value = [
            Workspace('123', 'a workspace'),
            Workspace('753', 'another workspace')
        ]

        sut = WorkspaceConsoleRenderer(toggl_repository)

        try:
            actual_output = io.StringIO()
            sys.stdout = actual_output

            sut.render()

            expected_output = \
                "123:a workspace\n" \
                "753:another workspace\n"

            self.assertEqual(actual_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
