import tkinter as tk


class Navbar(tk.Frame):
    def __init__(self, parent, *, listener):
        super().__init__(parent)

        self.config(background="#384B70")

        btn1 = tk.Button(self, text="Button1", command=listener.button_1)
        btn1.pack(side=tk.LEFT)
        btn2 = tk.Button(self, text="Button2", command=listener.button_2)
        btn2.pack(side=tk.LEFT)
        btn3 = tk.Button(self, text="Button3", command=listener.button_3)
        btn3.pack(side=tk.LEFT)
        btn4 = tk.Button(self, text="Button4", command=listener.button_4)
        btn4.pack(side=tk.LEFT)
        btn5 = tk.Button(self, text="Button5", command=listener.button_5)
        btn5.pack(side=tk.LEFT)


