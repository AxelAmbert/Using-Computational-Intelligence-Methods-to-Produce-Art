from tkinter import *

class Main:

    def init_canvas(self):
        self.w.pack(expand=YES, fill=BOTH)
        self.w.bind("<B1-Motion>", onMove)
        self.w.bind("<B1-ButtonRelease>", stopLine)
        self.w.bind("<ButtonPress-1>", startLine)
        self.w.bind("<ButtonPress-2>", overlap)


    def __init__(self):
        self.master = Tk()
        self.master.title("Painting using Ovals")
        self.w = Canvas(self.master,
                        width=canvas_width,
                        height=canvas_height)
        self.init_canvas()
        self.message = Label(self.master, text="Press and Drag the mouse to draw")
        self.message.pack(side=BOTTOM)

    def startLine(event):
        global Run, x1, y1, w
        Run = True
        x1, y1 = (event.x - 1), (event.y - 1)

    def stopLine(event):
        global Run, TmpLine

        Run = False
        print('num ?')
        print(TmpLine)

    def onMove(event):
        global x1, x2, y1, y2, w, TmpLine

        python_green = "#476042"
        if Run == False:
            return
        x2, y2 = (event.x + 1), (event.y + 1)
        w.delete(TmpLine)
        TmpLine = w.create_line(x1, y1, x2, y2, width=4, fill=python_green)

    def main(self):
        mainloop()


if __name__ == "__main__":
    Main().main()
