
class WorkspaceConsoleRenderer():

    def __init__(self, toggl_repository):
        self.toggl_repository = toggl_repository

    def render(self):
        workspaces = self.toggl_repository.workspaces()

        for workspace in workspaces:
            print(f'{workspace.id}:{workspace.name}')
