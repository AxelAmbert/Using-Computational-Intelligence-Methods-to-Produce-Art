class Connection:

    def __init__(self):
        self.parent = None
        self.child = None
        self.connection_parent = 'unset'
        self.connection_child = 'unset'

    def new(self, parent, child, c_from, c_end):
        self.parent = parent
        self.child = child
        self.connection_parent = c_from
        self.connection_child = c_end
        return self

    def reverse(self):
        return Connection().new(self.child, self.parent, self.connection_child, self.connection_parent)

    def __str__(self):
        return '\nparent: ' + str(self.parent.id) + '\n' + 'child: ' + str(self.child.id) + '\n' + 'connection: ' + self.connection_parent + '-> ' + self.connection_child + '\n'
