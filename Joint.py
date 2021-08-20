"""
    This class represents a joint
"""

class Joint:

    def __init__(self, parent, joint_id, where):
        self.parent = parent
        self.where = where
        self.id = joint_id
