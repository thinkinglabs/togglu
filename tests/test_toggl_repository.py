
import unittest

from .helpers.http import mock_http_server
from .helpers.http import WorkspacesRequestHandler
from .helpers.http import HttpGoneRequestHandler

from .context import togglu  # noqa: F401
from togglu.toggl_repository import TogglRepository
from togglu.workspace import Workspace


class TogglRepositoryTestCase(unittest.TestCase):

    def test_workspaces(self):
        mock_server_port = mock_http_server(WorkspacesRequestHandler)
        stub_url = f'http://localhost:{mock_server_port}'

        sut = TogglRepository(base_url=stub_url)
        actual = sut.workspaces()

        expected = [
            Workspace(1234567, 'workspace 1'),
            Workspace(2345678, 'workspace 2'),
            Workspace(3456789, 'workspace 3')
        ]
        self.assertEqual(actual, expected)

    def test_410_gone(self):
        mock_server_port = mock_http_server(HttpGoneRequestHandler)

        stub_url = f'http://localhost:{mock_server_port}'

        sut = TogglRepository(stub_url)
        with self.assertRaises(Exception):
            sut.workspaces()
