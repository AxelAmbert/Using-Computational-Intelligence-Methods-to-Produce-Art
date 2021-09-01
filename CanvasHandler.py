import time
from tkinter import *
from Line import *
from Joint import *
from Connection import *
from GeneticModifierHandler import *
import random
from tkinter.messagebox import showinfo

"""
    This class is used to both:
        Draw a Biomorph in the BiomorphCreator View.
        Evolve a Biomorph in the Evolution View

    It handles drawing logic and let the user:
        Draw lines
        Connect lines
        Keep track of the modifications (history)
        Jump into a line history, to go to a previous step
    
    It can be locked to prevent the user from drawing on it.
"""


class CanvasHandler:

    def remove_previous_joints(self):
        for tag in self.canvas.find_withtag('joint'):
            self.canvas.delete(tag)

    """
        Draw a joint if there is no joint at the current [x, y] position
    """

    def draw_a_join_not_overlapping(self, x, y):
        col = "#476042"

        if self.look_for_tags_overlapping([x, y, x, y], ['joint']) is None:
            id_value = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                                               width=((self.size[0] + self.size[1]) / 300),
                                               outline=col,
                                               fill=col,
                                               tags='joint')
            self.canvas.addtag_withtag(id_value, id_value)
            return id_value
        return None

    """
        For each line, draw the corresponding joints, if they are not overlapping with other joints
    """

    def draw_joints(self):
        for line in self.lines:
            x, y = line.get_start()
            begin = self.draw_a_join_not_overlapping(x, y)
            x, y = line.get_end()
            end = self.draw_a_join_not_overlapping(x, y)
            line.set_join_values(Joint(line, begin, 'start'), Joint(line, end, 'end'))

    def redraw_joints(self):
        self.remove_previous_joints()
        self.draw_joints()

    def has_right_tags(self, tags, tag_to_find):
        for tag in tags:
            if tag == tag_to_find:
                return True
        return False

    """
        Look if at a certain position (pos), there is certain tags (tags) overlapping.
    """

    def look_for_tags_overlapping(self, pos, tags, debug=False):
        overlaps = self.canvas.find_overlapping(*pos)
        for overlap in overlaps:
            tags_overlap = self.canvas.gettags(overlap)
            for tag in tags:
                if self.has_right_tags(tags_overlap, tag) is True:
                    if debug is True:
                        print(overlap)
                    return overlap
        return None

    """
        Verify if the user clicked on a joint by looking if the position in event overlaps with a "joint" tag.
    """

    def verify_line_validity(self, event):
        if len(self.lines) == 0:
            return True
        return self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint']) is not None

    def find_line_ownership(self, joint_id):
        for line in self.lines:
            if line.has_joint_ownership(joint_id):
                return line
        return None

    """
        Find the line that is the owner of the joint the user clicked on.
        Assign the line to the "selected_line" class attribute
        Complete the future connection
    """

    def set_new_parent_line(self, event):
        overlap_joint_id = self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint'], debug=False)
        if overlap_joint_id is None:
            return
        line_ownership = self.find_line_ownership(overlap_joint_id)
        if line_ownership is None:
            return
        self.selected_line = line_ownership
        self.connection_tmp.parent = line_ownership
        self.connection_tmp.root = line_ownership
        self.connection_tmp.connection_parent = line_ownership.get_joint_pos(overlap_joint_id)

    """
        Called when the user click on the canvas
        Verify if the user clicked on a valid position
        Allow drawing only if the user clicked on a joint or if there is no joint at all (first line drawn)
    """

    def on_press(self, event):
        if self.lock_mode is True:
            self.on_selected()
            return
        elif self.verify_line_validity(event) is False:
            return
        self.set_new_parent_line(event)
        self.allow_drawing = True
        self.x1, self.y1 = event.x, event.y

    """
        This function is called to connect a new line to every other line.
        If the owner of the joint is line 1, that is connected to line 2 and line 3.
        The new line will be connected to line 1, and line 2, 3 by extension.
    """

    def link_to_every_overlap(self, line):
        for connection in self.selected_line.connections:
            new_connection = self.connection_tmp.copy()
            new_connection.parent = connection.child
            new_connection.root = connection.child
            new_connection.connection_parent = connection.connection_child
            if connection.connection_parent == self.connection_tmp.connection_parent:
                connection.child.add_connection(new_connection)
                line.add_connection(new_connection.reverse())
        self.selected_line.add_connection(self.connection_tmp.copy())
        line.add_connection(self.connection_tmp.reverse())

    """
        Create a new line and add the proper connections
    """

    def create_a_new_line(self):
        if self.allow_drawing is False:
            return
        line = Line(self.drawn_line_tmp, self.selected_line, [self.x1, self.x2, self.y1, self.y2],
                    self.drawn_line_tmp)
        self.lines.append(line)
        self.connection_tmp.child = line
        self.connection_tmp.connection_child = 'start'
        if self.selected_line is not None:
            self.link_to_every_overlap(line)
        self.on_change()
        return line

    def double_overlapping_error(self, overlap_joint_id):
        return self.connection_tmp.parent.has_joint_ownership(overlap_joint_id)

    """
        Look if the end of the created line is on another joint
        It will then create another connection based on that closing overlap
    """

    def link_to_every_closing_overlap(self, line, created_connection, overlap_line):
        for connection in overlap_line.connections:
            new_connection = created_connection.copy()
            new_connection.parent = connection.child
            new_connection.root = connection.child
            new_connection.connection_parent = connection.connection_child
            if connection.connection_parent == created_connection.connection_parent:
                connection.child.add_connection(new_connection)
                line.add_connection(new_connection.reverse())
        line.add_connection(created_connection.copy())
        overlap_line.add_connection(created_connection.reverse())

    def look_for_closing_overlap(self, created_line, event):
        overlap_joint_id = self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint'])
        overlap_line = self.find_line_ownership(overlap_joint_id)
        if overlap_joint_id is None or \
                self.double_overlapping_error(overlap_joint_id) is True or \
                overlap_line is None:
            return
        new_connection = Connection().new(created_line, overlap_line, overlap_line, 'end',
                                          overlap_line.get_joint_pos(overlap_joint_id))
        self.link_to_every_closing_overlap(created_line, new_connection, overlap_line)
        #created_line.add_connection(new_connection)
        #overlap_line.add_connection(new_connection.reverse())

    """
        This function is called when the user release the mouse button.
        If the previous requirement are not met (i.e: drawing is locked), it will be ignored.
        Otherwise, it will create a new line and reset the temporary attributes.
    """

    def on_release(self, event):
        if self.lock_mode is True:
            return
        created_line = self.create_a_new_line()
        self.look_for_closing_overlap(created_line, event)
        self.allow_drawing = False
        self.drawn_line_tmp = -1
        self.selected_line = None
        self.redraw_joints()
        self.connection_tmp = Connection()

    """
        This function is called when the user move its mouse.
        If the previous requirement are not met (i.e: drawing is locked), it will be ignored.
        Otherwise, it will draw a temporary line that represent the moving mouse.
    """

    def on_move(self, event):
        if self.allow_drawing is False:
            return

        self.x2, self.y2 = event.x, event.y
        self.canvas.delete(self.drawn_line_tmp)

        self.drawn_line_tmp = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                                                      width=(self.size[0] + self.size[1]) / 200, fill="#476042")

    def overlap(self, event):
        print(self.canvas.find_overlapping(event.x, event.y, event.x, event.y))

    def select_line(self, _):
        line = self.lines[2]
        line.genetic_modifier[0].apply_evolution()
        self.recompute_canvas()

    def check(self, event):
        print("Check " + str(len(self.lines)))

    def get_id(self, event):
        print(self.canvas.find_overlapping(event.x, event.y, event.x, event.y))

    def init_canvas(self):
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<B1-ButtonRelease>", self.on_release)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonPress-2>", lambda e: self.recompute_canvas(test=True))
        self.canvas.bind("<ButtonPress-3>", self.get_id)

    def get_lines(self):
        return self.lines

    """
        Redraw the canvas entirely
        Also draw joints if the canvas is in drawing mode
    """

    def recompute_canvas(self, test=False):
        i = 0

        for line in self.lines:
            self.canvas.delete(line.id)

            if i == 3:
                line.id = self.canvas.create_line(*line.get_pos(),
                                                  width=((self.size[0] + self.size[1]) / 200) if test is False else (
                                                          (self.size[0] + self.size[1]) / 100),
                                                  fill="#9353e7" if test is False else line.color, tags='line')
            else:
                line.id = self.canvas.create_line(*line.get_pos(),
                                                  width=((self.size[0] + self.size[1]) / 200) if test is False else (
                                                          (self.size[0] + self.size[1]) / 100),
                                                  fill=line.color, tags='line')

            line.redraw = False
            i += 1
        if self.lock_mode is False:
            self.redraw_joints()
        if test is True:
            for line in self.lines:
                print(line)

    def lock(self):
        self.lock_mode = True

    def unlock(self):
        self.lock_mode = False

    def set_size(self, x, y):
        self.canvas.config(width=x, height=y)

    def set_grid(self, column, row):
        self.canvas.grid(column=column, row=row)

    def scale_lines(self, old_size, new_size):
        for line in self.lines:
            line.scale(old_size, new_size)

    def repair_connection(self, lines, line, connection):
        connection.parent = line
        for line_tmp in lines:
            if line_tmp.id == connection.child.id:
                connection.child = line_tmp
                connection.root = line_tmp if connection.root.id == line_tmp.id else line
                return

    def recompute_connections(self, lines):
        for line in lines:
            for connection in line.connections:
                self.repair_connection(lines, line, connection)

    def new_line_array(self, lines):
        arr = []

        for line in lines:
            cp = line.copy()
            arr.append(cp)
        self.recompute_connections(arr)
        return arr

    def verification(self):

        for line in self.lines:
            child_found = False
            root_found = False
            for connection in line.connections:
                for find_line in self.lines:
                    if connection.child.id == find_line.id:
                        child_found = True
                    if connection.root.id == find_line.id:
                        root_found = True
                if child_found is False or root_found is False:
                    print('IT FAILED ' + 'Error for canvas ' + str(
                        self.id) + 'child not found ' if child_found is False else ' ' + ', root not found ' if root_found is False else '.' + self.last_action)
                    # showinfo('Error', 'Error for canvas ' + str(self.id) + 'child not found ' if child_found is False else ' ' + ', root not found ' if root_found is False else '.' + self.last_action)
                    return

    """
        Reconstruct the canvas with a new set of line
        It handles new size and scale the lines to a new ratio
    """

    def reconstruct(self, lines, old_size, new_size):
        self.canvas.delete('all')
        self.drawn_line_tmp = 0
        self.lines = self.new_line_array(lines)
        self.selected_line = None
        self.connection_tmp = Connection()
        self.scale_lines(old_size, new_size)
        self.size = new_size
        self.recompute_canvas()
        self.verification()

    """
        This function is called when there is a change in the canvas
        Example: a new line has been drawn, or a line has been removed
    """

    def on_change(self):
        if self.history_enabled is False:
            return
        if self.history_index != len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]

        self.history.append(self.new_line_array(self.lines))
        self.history_index = len(self.history) - 1

    """
        Call every callback when the canvas is selected while it is in lock_mode=True
    """

    def on_selected(self):
        for callback in self.on_selected_callbacks:
            callback(self)

    def add_selected_callback(self, callback):
        self.on_selected_callbacks.append(callback)

    def set_history_status(self, status):
        self.history_enabled = status
        if status is True:
            self.history.append(self.new_line_array(self.lines))

    def delete_history(self):
        self.history = []

    def history_jump(self, jump_size):
        new_index = self.history_index + jump_size

        if new_index < 0 or new_index >= len(self.history):
            return
        self.history_index = new_index
        self.reconstruct(self.history[self.history_index], self.size, self.size)

    def __init__(self, master, theId=0):
        self.size = [500, 500]
        self.canvas = Canvas(master,
                             width=500,
                             height=500)
        self.init_canvas()
        self.allow_drawing = False
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.drawn_line_tmp = 0
        self.lines = []
        self.selected_line = None
        self.connection_tmp = Connection()
        self.lock_mode = False
        self.done = False
        self.lines_nb = 0
        self.on_selected_callbacks = []
        self.history = []
        self.history_enabled = False
        self.history_index = 0
        self.id = theId
        self.last_action = None
