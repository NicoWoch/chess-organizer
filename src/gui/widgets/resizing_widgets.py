import tkinter as tk

from src.gui.widgets.resizing_font import ResizingFont


class ResizingLabel(tk.Label):  # TODO: remove code repetition
    def __init__(self, parent, relwidth=.8, relheight=.8, minsize=4, maxsize=100, **kwargs):
        if kwargs.get('bg', None) in ('transparent', None):
            kwargs['bg'] = parent.cget('background')

        super().__init__(parent, **kwargs)

        base_font = kwargs.get('font', ('Comic Sans MS',))
        self._font = ResizingFont(self, self.get_text, base_font, relwidth,
                                  relheight, minsize, maxsize)
        self._font.resize_font()

        self.config(font=self._font)

    def get_text(self) -> str:
        return self.cget('text')

    def destroy(self):
        self._font.unbind()
        super().destroy()


class ResizingButton(tk.Button):
    def __init__(self, parent, relwidth=.8, relheight=.8, minsize=4, maxsize=100, **kwargs):
        if kwargs.get('bg', None) in ('transparent', None):
            kwargs['bg'] = parent.cget('background')
            kwargs.setdefault('bd', 0)

        super().__init__(parent, **kwargs)

        base_font = kwargs.get('font', ('Comic Sans MS',))
        self._font = ResizingFont(self, self.get_text, base_font, relwidth,
                                  relheight, minsize, maxsize)
        self._font.resize_font()

        self.config(font=self._font)

    def get_text(self) -> str:
        return self.cget('text')

    def destroy(self):
        self._font.unbind()
        super().destroy()
