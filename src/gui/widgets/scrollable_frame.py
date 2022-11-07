import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, child_frame_class: type[tk.Widget], *args, **kwargs):
        super().__init__(parent)

        self._canvas = tk.Canvas(self)
        self.child_frame = child_frame_class(self._canvas, *args, **kwargs)
        self._scrollbar = tk.Scrollbar(self, orient='vertical', command=self._canvas.yview)

        self.height = 100
        self.scrollbar_width = 20
        self.scrollbar_speed = 1
        self._configure_after = None
        self._has_scrollbar = False

        self._canvas.place(relwidth=1, relheight=1)

        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self.update_window()

        self.bind('<Configure>', self._handle_configure)

    def _handle_configure(self, _):
        if self._configure_after is not None:
            self.after_cancel(self._configure_after)

        self._configure_after = self.after(100, self.update_window)

    def _handle_scroll(self, event):
        if self._has_scrollbar:
            self._canvas.yview_scroll(-event.delta * self.scrollbar_speed // 120, 'units')

    def get_scroll_amount(self):
        return self._canvas.yview()[0] * self.height

    def _should_has_scrollbar(self):
        return self.height > self._canvas.winfo_height()

    def _update_scrollbar(self):
        if self._should_has_scrollbar() == self._has_scrollbar:
            return

        self._canvas.place_forget()
        self._scrollbar.place_forget()

        if self._should_has_scrollbar():
            self._canvas.place(width=-self.scrollbar_width, relwidth=1, relheight=1)
            self._scrollbar.place(x=-self.scrollbar_width, relx=1, width=self.scrollbar_width, relheight=1)
        else:
            self._canvas.place(relwidth=1, relheight=1)

        self._has_scrollbar = self._should_has_scrollbar()

    def update_window(self):
        self._update_scrollbar()

        self.child_frame['width'] = self.winfo_width() - (self.scrollbar_width if self._has_scrollbar else 0)
        self.child_frame['height'] = self.height

        self._canvas.delete('all')
        self._canvas.create_window((0, 0), window=self.child_frame, anchor='nw')

        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._canvas.bind_all('<MouseWheel>', self._handle_scroll)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x300')

    ScrollableFrame(root, tk.Label, text='lorem ipsum difuculte ess\n' * 100).place(relwidth=1, relheight=1)

    root.mainloop()
