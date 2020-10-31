
import unittest

from togglu.workspace import Workspace


class WorkspaceTestCase(unittest.TestCase):

    def test_workspaces_having_the_same_fields_are_equal(self):
        self.assertEqual(Workspace('123', 'aWorkspace'), Workspace('123', 'aWorkspace'))

    def test_workspace_and_aclass_are_not_equal(self):
        self.assertNotEqual(Workspace('123', 'aWorkspace'), AClass('123', 'aWorkspace'))


class AClass():

    def __init__(self, id, name):
        self.id = id
        self.name = name


if __name__ == '__main__':
    unittest.main()
