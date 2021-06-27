from tkinter import *
from Line import *
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
        col = self.random_color()

        if self.look_for_tags_overlapping([x, y, x, y], ['joint']) == False:
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, width=5, outline=col, fill=col, tags='joint')

    def draw_joints(self):
        for line in self.lines:
            x, y = line.get_start()
            self.draw_a_join_not_overlaping(x, y)
            x, y = line.get_end()
            self.draw_a_join_not_overlaping(x, y)

    def redraw_joints(self):
        self.remove_previous_joints()
        self.draw_joints()

    def has_right_tags(self, tags, tag_to_find):
        for tag in tags:
            if tag == tag_to_find:
                return True
        return False

    def look_for_tags_overlapping(self, pos, tags):
        overlaps = self.canvas.find_overlapping(*pos)
        for overlap in overlaps:
            tags_overlap = self.canvas.gettags(overlap)
            for tag in tags:
                if self.has_right_tags(tags_overlap, tag) == True:
                    return True
        return False


    def verify_line_validity(self, event):
        if len(self.lines) == 0:
            return True
        return self.look_for_tags_overlapping([event.x, event.y, event.x, event.y], ['joint'])


    def on_press(self, event):
        if self.verify_line_validity(event) == False:
            return
        self.allow_drawing = True
        self.x1, self.y1 = (event.x - 1), (event.y - 1)

    def on_release(self, _):
        self.allow_drawing = False
        self.drawn_line_tmp = -1
        self.lines.append(Line([self.x1, self.x2, self.y1, self.y2], self.drawn_line_tmp))
        self.redraw_joints()

    def on_move(self, event):
        if self.allow_drawing == False:
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

    def __init__(self, master):
        self.canvas = Canvas(master,
                             width=500,
                             height=500)
        self.init_canvas()
        self.allow_drawing = False
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.drawn_line_tmp = 0
        self.lines = []
