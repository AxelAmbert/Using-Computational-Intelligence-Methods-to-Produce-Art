from tkinter import *
from Line import *
from Joint import *
from Connection import *

import random


class CanvasHandler:

    def random_color(self):
        t = '#'

        for i in range(0, 6):
            t += str(random.randint(0, 9))
        return t

    def remove_previous_joints(self):
        for tag in self.canvas.find_withtag('joint'):
            self.canvas.delete(tag)

    def draw_a_join_not_overlaping(self, x, y):
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

    def draw_joints(self):
        for line in self.lines:
            x, y = line.get_start()
            begin = self.draw_a_join_not_overlaping(x, y)
            x, y = line.get_end()
            end = self.draw_a_join_not_overlaping(x, y)
            line.set_join_values(Joint(line, begin, 'start'), Joint(line, end, 'end'))

    def redraw_joints(self):
        self.remove_previous_joints()
        self.draw_joints()

    def has_right_tags(self, tags, tag_to_find):
        for tag in tags:
            if tag == tag_to_find:
                return True
        return False

    def look_for_tags_overlapping(self, pos, tags, debug=False):
        overlaps = self.canvas.find_overlapping(*pos)
        for overlap in overlaps:
            tags_overlap = self.canvas.gettags(overlap)
            for tag in tags:
                if self.has_right_tags(tags_overlap, tag) == True:
                    if debug is True:
                        print(overlap)
                    return overlap
        return None

    def verify_line_validity(self, event):
        if len(self.lines) == 0:
            return True
        return self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint']) is not None

    def find_line_ownership(self, joint_id):
        for line in self.lines:
            if line.has_joint_ownership(joint_id):
                return line
        return None

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

    def on_press(self, event):
        if self.lock_mode is True:
            self.on_selected()
            return
        elif self.verify_line_validity(event) is False:
            return
        self.set_new_parent_line(event)
        self.allow_drawing = True
        self.x1, self.y1 = (event.x - 1), (event.y - 1)

    def create_a_new_line(self):
        if self.allow_drawing is False:
            return
        line = Line.Line(self.drawn_line_tmp, self.selected_line, [self.x1, self.x2, self.y1, self.y2],
                         self.drawn_line_tmp)
        self.lines.append(line)
        self.connection_tmp.child = line
        self.connection_tmp.connection_child = 'start'
        if self.selected_line is not None:
            self.selected_line.add_connection(self.connection_tmp)
            line.add_connection(self.connection_tmp.reverse())
        return line

    def double_overlapping_error(self, overlap_joint_id):
        return self.connection_tmp.parent.has_joint_ownership(overlap_joint_id)

    def look_for_closing_overlap(self, created_line, event):
        overlap_joint_id = self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint'])
        overlap_line = self.find_line_ownership(overlap_joint_id)
        if overlap_joint_id is None or \
                self.double_overlapping_error(overlap_joint_id) is True or \
                overlap_line is None:
            return
        new_connection = Connection().new(created_line, overlap_line, overlap_line, 'end',
                                          overlap_line.get_joint_pos(overlap_joint_id))
        created_line.add_connection(new_connection)
        overlap_line.add_connection(new_connection.reverse())

    def on_release(self, event):
        created_line = self.create_a_new_line()
        self.look_for_closing_overlap(created_line, event)
        self.allow_drawing = False
        self.drawn_line_tmp = -1
        self.selected_line = None
        self.redraw_joints()
        self.connection_tmp = Connection()

    def on_move(self, event):
        if self.allow_drawing is False:
            return

        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        self.canvas.delete(self.drawn_line_tmp)

        self.drawn_line_tmp = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                                                      width=(self.size[0] + self.size[1]) / 200, fill="#476042")

    def overlap(self, event):
        print(self.canvas.find_overlapping(event.x, event.y, event.x, event.y))

    def select_line(self, event):
        line = self.lines[2]
        line.genetic_modifier[0].apply_evolution(force=True)
        self.recompute_canvas()

    def init_canvas(self):
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<B1-ButtonRelease>", self.on_release)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonPress-2>", self.select_line)

    def get_lines(self):
        return self.lines

    def delete_moved_lines(self):
        for line in self.lines:
            if line.redraw is True:
                print(line.id)

    def recompute_canvas(self, simulation=False):
        force = self.handle_lines_nb_change()
        # self.canvas.delete("all")
        if force is True:
            self.canvas.delete('all')
        for line in self.lines:
            if line.redraw is True or force is True:
                self.canvas.delete(line.id)

                line.id = self.canvas.create_line(*line.get_pos(), width=(self.size[0] + self.size[1]) / 200,
                                                  fill="#476042")
                line.redraw = False
                for g in line.genetic_modifier:
                    g.apply_evolution()

        if simulation is False or force is True:
            self.redraw_joints()

    def lock(self):
        self.lock_mode = True

    def unlock(self):
        self.lock_mode = False

    def set_size(self, x, y):
        self.canvas.config(width=x, height=y)

    def set_grid(self, column, row):
        self.canvas.grid(column=column, row=row)

    def scale_lines(self, new_size):
        for line in self.lines:
            line.scale(self.size, new_size)

    def new_line_array(self, lines):
        arr = []

        for line in lines:
            arr.append(line.copy(self.lines))
        return arr

    def reconstruct(self, lines, new_size):
        self.drawn_line_tmp = 0
        self.lines = self.new_line_array(lines)
        self.selected_line = None
        self.connection_tmp = Connection()
        self.scale_lines(new_size)
        self.size = new_size
        self.recompute_canvas()

    def handle_lines_nb_change(self):
        if len(self.lines) != self.lines_nb:
            self.lines_nb = len(self.lines)
            return True
        return False

    def on_selected(self):
        for callback in self.on_selected_callbacks:
            callback(self)

    def add_selected_callback(self, callback):
        self.on_selected_callbacks.append(callback)

    def __init__(self, master):
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
