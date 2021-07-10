from tkinter import *
from Line import *
from Joint import *
import random
from tkinter.messagebox import showinfo


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

        if self.look_for_tags_overlapping([x, y, x, y], ['joint']) == None:
            return self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, width=5, outline=col, fill=col, tags='joint')
        return -1

    def draw_joints(self):
        for line in self.lines:
            x, y = line.get_start()
            begin = self.draw_a_join_not_overlaping(x, y)
            x, y = line.get_end()
            end = self.draw_a_join_not_overlaping(x, y)
            line.set_join_values(begin, end)

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
        return self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint']) != None

    def find_line_ownership(self, joint_id):
        for line in self.lines:
            if line.has_joint_ownership(joint_id):
                return line
        return None

    def set_new_parent_line(self, event):
        overlap_joint_id = self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint'], debug=True)
        if overlap_joint_id is None:
            return
        line_ownership = self.find_line_ownership(overlap_joint_id)
        if line_ownership is None:
            return
        self.selected_line = line_ownership

    def on_press(self, event):
        if self.verify_line_validity(event) == False:
            return
        self.set_new_parent_line(event)
        self.allow_drawing = True
        self.x1, self.y1 = (event.x - 1), (event.y - 1)

    def create_a_new_line(self):
        if self.allow_drawing is False:
            return
        line = Line(self.selected_line, [self.x1, self.x2, self.y1, self.y2], self.drawn_line_tmp)
        if self.selected_line is not None:
            self.selected_line.add_a_link_begin(line)
        self.lines.append(line)

    def on_release(self, _):
        self.create_a_new_line()
        self.allow_drawing = False
        self.drawn_line_tmp = -1
        self.selected_line = None
        self.redraw_joints()
        for line in self.lines:
            print(line)

    def on_move(self, event):
        if self.allow_drawing is False:
            return

        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        self.canvas.delete(self.drawn_line_tmp)
        self.drawn_line_tmp = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=4, fill="#476042")

    def overlap(self, event):
        print(self.canvas.find_overlapping(event.x, event.y, event.x, event.y))

    def init_canvas(self):
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<B1-ButtonRelease>", self.on_release)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonPress-2>", self.overlap)

    def get_lines(self):
        return self.lines

    def recompute_canvas(self):
        self.canvas.delete("all")
        for line in self.lines:
            self.canvas.create_line(*line.get_pos(), width=4, fill="#476042")
        self.redraw_joints()

    def __init__(self, master):
        self.canvas = Canvas(master,
                             width=500,
                             height=500)
        self.init_canvas()
        self.allow_drawing = False
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.drawn_line_tmp = 0
        self.lines = []
        self.selected_line = None
