from collections import namedtuple
from tkinter import font as tkfont
from BiomorphCreator import *
from EvolutionView import *
import unittest
FakeEvent = namedtuple('event', 'x y')


class BiomorphCreatorTests(unittest.TestCase):

    def __init__(self, container, controller):
        super().__init__()
        self.container = container
        self.controller = controller
        self.canvas = self.controller.frames['BiomorphCreator'].canvas
        self.start_tests()

    def start_tests(self):
        self.test_draw_simple_line()
        self.test_connect_a_line()
        self.test_fail_to_connect_line()
        self.test_previous_history()

    def test_draw_simple_line(self):
        fake_event_press = FakeEvent(50, 100)
        fake_event_move = FakeEvent(500, 150)

        self.canvas.on_press(fake_event_press)
        self.canvas.on_move(fake_event_move)
        self.canvas.on_release(fake_event_move)
        self.assertTrue(len(self.canvas.lines) == 1, 'Fails to create a simple line, len != 1')
        created_line = self.canvas.lines[0]
        x_s, y_s, x_e, y_e = self.canvas.lines[0].get_pos()
        self.assertTrue(created_line.parent is None, 'Line"s parent should be none')
        self.assertTrue(x_s == 50 and y_s == 100 and x_e == 500 and y_e == 150, 'Wrong line positions')
        self.assertTrue(len(created_line.connections) == 0, 'Line should have no connections')

    def test_connect_a_line(self):
        fake_event_press = FakeEvent(500, 150)
        fake_event_move = FakeEvent(250, 75)

        self.canvas.on_press(fake_event_press)
        self.canvas.on_move(fake_event_move)
        self.canvas.on_release(fake_event_move)
        self.assertTrue(len(self.canvas.lines) == 2, 'Fails to link a line, len != 2')
        created_line = self.canvas.lines[1]
        for line in self.canvas.lines:
            self.assertTrue(len(line.connections) == 1, 'Wrong number of connection in line ' + str(line.id))
        self.assertTrue(created_line.connections[0].root.id == self.canvas.lines[0].id, 'Wrong root of connection')
        self.assertTrue(created_line.connections[0].child.id == self.canvas.lines[0].id, 'Wrong child for created line')
        self.assertTrue(self.canvas.lines[0].connections[0].child.id == created_line.id, 'Wrong child for first line')

    def test_fail_to_connect_line(self):
        fake_event_press = FakeEvent(30, 30)
        fake_event_move = FakeEvent(50, 50)

        self.canvas.on_press(fake_event_press)
        self.canvas.on_move(fake_event_move)
        self.canvas.on_release(fake_event_move)
        self.assertTrue(len(self.canvas.lines) == 2, 'Created a line that is connected to nothing, len != 2')

    def test_previous_history(self):
        self.canvas.history_jump(-1)
        self.assertTrue(len(self.canvas.lines) == 1, 'Fails to jump back in history, len != 1')
        self.canvas.history_jump(-1)
        self.assertTrue(len(self.canvas.lines) == 0, 'Fails to double jump back in history, len != 0')
        self.canvas.history_jump(1)
        self.assertTrue(len(self.canvas.lines) == 1, 'Fails to double jump back in history, then go next, len != 1')
        self.canvas.history_jump(1)
        self.assertTrue(len(self.canvas.lines) == 2, 'Fails to  jump back twice in history, then go next twice, '
                                                     'len != 1')

    def test_min_max_values(self):
        x_min, y_min, x_max, y_max = self.controller.frames['BiomorphCreator'].get_min_max_values()

        self.assertTrue(x_min == 50, 'x_min should be 50')
        self.assertTrue(y_min == 75, 'y_min should be 75')
        self.assertTrue(x_max == 200, 'x_max should be 500')
        self.assertTrue(y_max == 150, 'y_max should be 50')



class GCodeTests(unittest.TestCase):

    def __init__(self, container, controller):
        super().__init__()
        self.container = container
        self.controller = controller
        self.canvas = self.controller.frames['BiomorphCreator'].canvas
        self.test_generated_g_code()

    def start_tests(self):
        self.test_generated_g_code()

    def test_generated_g_code(self):
        BiomorphIOConverterGCode(self.canvas, 'unit_test_g_code.txt').encode()
        with open('unit_test_g_code.txt', 'r') as file:
            full_file = ''.join(file.read().split())
            print(full_file)
            self.assertTrue(full_file == 'G0X0.0Y-100.0G1X450.0Y-150.0G0X450.0Y-150.0G1X200.0Y-75.0')

class UnitTests:

    def __init__(self, container, controller):
        BiomorphCreatorTests(container, controller)
        GCodeTests(container, controller)


class ViewHandler(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.resizable(False, False)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (BiomorphCreator, EvolutionView):
            page_name = F.__name__
            frame = F(parent=container, controller=self, )
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("BiomorphCreator")
        UnitTests(container, self)

    def show_frame(self, page_name, data=None):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.update_with_data(data)
        frame.tkraise()


if __name__ == "__main__":
    app = ViewHandler()
    app.mainloop()
