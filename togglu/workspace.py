
class Workspace:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        return other.__class__.__name__ == 'Workspace' and \
            self.id == other.id and \
            self.name == other.name

    def __repr__(self):
        return f"Workspace(id={self.id}, name={self.name})"
