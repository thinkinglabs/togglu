
import unittest

from togglu.workspace import Workspace


class WorkspaceTestCase(unittest.TestCase):

    def test_workspaces_having_the_same_fields_are_equal(self):
        self.assertEqual(Workspace('123', 'aWorkspace'), Workspace('123', 'aWorkspace'))


if __name__ == '__main__':
    unittest.main()
