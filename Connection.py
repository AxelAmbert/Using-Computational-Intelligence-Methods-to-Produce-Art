
"""
    Represent a connection between two line
    parent is the owner of the connection
    child is the line where parent points to
    root is the owner of the connection (usually the older line)
    connection_parent is from where the connection is on the parent (start, end)
    connection_child is from where the connection is on the child (start, end)
"""


class Connection:

    def __init__(self):
        self.parent = None
        self.child = None
        self.root = None
        self.connection_parent = 'unset'
        self.connection_child = 'unset'

    def new(self, parent, child, root, c_from, c_end):
        self.parent = parent
        self.child = child
        self.root = root
        self.connection_parent = c_from
        self.connection_child = c_end
        return self

    def reverse(self):
        return Connection().new(self.child, self.parent, self.root, self.connection_child, self.connection_parent)

    def copy(self):
        return Connection().new(self.parent, self.child, self.root, self.connection_parent, self.connection_child)

    def __str__(self):
        return '\nparent: ' + str(self.parent.id) + '\n' + 'child: ' + str(
            self.child.id) + '\n' + 'connection: ' + self.connection_parent + '-> ' + self.connection_child + ', root ->' + str(self.root.id) + '\n'
