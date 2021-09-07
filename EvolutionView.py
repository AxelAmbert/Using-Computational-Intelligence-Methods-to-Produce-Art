from CanvasGrid import *
from BiomorphIOConverterGCode import *

"""
    This class is representing the Tkinter view: Evolution.
    In this view the user makes its Biomorph Evolve
"""

class EvolutionView(tk.Frame):


    def update_data(self, canvas):
        for genetic_handler in self.genetic_handlers:
            if genetic_handler.canvas_handler.id == canvas.id:
                genetic_handler.reinforce()
                break
        self.update_with_data(canvas)


    def verify_line_position(self, line, connection):
        line_x_s, line_y_s, line_x_e, line_y_e = line.get_pos()
        connection_x_s, connection_y_s, connection_x_e, connection_y_e = connection.root.get_pos()
        size_x, size_y = line_x_e - line_x_s, line_y_e - line_y_s

        if connection.connection_child == 'start':
            line.set_pos([connection_x_s, connection_y_s, connection_x_s + size_x, connection_y_s + size_y])
        else:
            line.set_pos([connection_x_e, connection_y_e, connection_x_e + size_x, connection_y_e + size_y])

    """
        This function can be called as a safeguard.
        It will recompute every line positions to be sure its right.
    """
    def verify_a_canvas_integrity(self, canvas):
        for line in canvas.lines:
            print(line)
            for connection in line.connections:
                if connection.root.id != line.id:
                    self.verify_line_position(line, connection)

    def verify_every_canvas_integrity(self):
        for canvas in self.canvas_array:
            self.verify_a_canvas_integrity(canvas)

    def init_canvas_array(self):
        x = 0
        for i in range(0, 3):
            for y in range(0, 3):
                x += 1
                tmp_canvas = CanvasHandler(self, x)
                tmp_canvas.set_size(250, 250)
                tmp_canvas.canvas.grid(column=i, row=y, padx=(50, 50), pady=(25, 25))
                tmp_canvas.lock()
                tmp_canvas.set_history_status(True)
                tmp_canvas.add_selected_callback(self.update_data)
                self.canvas_array.append(tmp_canvas)

    def init_slider(self):
        s = Scale(self, from_=0, to=10, orient=HORIZONTAL)
        s.set(1)
        s.grid(column=1, row=4)
        return s

    def init_label(self):
        l = Label(self, text='Number of iterations')
        l.grid(column=1, row=3)

    def do_x_evolution_step(self, modifier):
        for i in range(0, self.slider.get()):
            modifier.start_evolution()

    """
        Called when the user click on a canvas
        It will reload the EvolutionView with new data
    """
    def update_with_data(self, new_canvas, jump=False):
        i = 0

        if new_canvas is None or new_canvas.lines is None:
            return
        for canvas in self.canvas_array:
            canvas.reconstruct(new_canvas.lines, new_canvas.size, [100, 100])
            if jump is False:
                canvas.on_change()
        for modifier in self.genetic_handlers:
            i += 1
            print('Evolution for ' + str(i))
            if i == 5:
                self.parent_canvas = modifier.canvas_handler
                continue
            self.do_x_evolution_step(modifier)

        #self.verify_every_canvas_integrity()

        print('no jump')
        for canvas in self.canvas_array:
            canvas.recompute_canvas()

    def create_genetic_handlers(self):
        array = []

        for canvas in self.canvas_array:
            array.append(GeneticModifierHandler(canvas))
        return array

    def history_jump_and_reconstruct(self, jump_size):
        self.parent_canvas.history_jump(jump_size)
        self.update_with_data(self.parent_canvas, jump=True)

    def prev_and_next_buttons(self):
        Button(self, text="refresh", command=self.refresh).grid(column=0, row=5)
        Button(self, text="prev", command=lambda: self.history_jump_and_reconstruct(-1)).grid(column=1, row=5)
        Button(self, text="next", command=lambda: self.history_jump_and_reconstruct(1)).grid(column=2, row=5)
        Button(self, text="to gcode", command=lambda: BiomorphIOConverterGCode(self.parent_canvas, 'test.txt').encode()).grid(column=3, row=5)
        Button(self, text="edit", command=lambda: self.controller.show_frame('BiomorphCreator', self.parent_canvas)).grid(column=4, row=5)


    def refresh(self):
        self.update_with_data(self.parent_canvas)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#000000')
        self.controller = controller
        self.canvas_array = []
        self.init_canvas_array()
        self.init_label()
        self.slider = self.init_slider()
        self.genetic_handlers = self.create_genetic_handlers()
        self.prev_and_next_buttons()
        self.parent_canvas = self.canvas_array[4]
