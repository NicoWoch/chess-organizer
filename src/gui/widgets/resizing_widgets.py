import tkinter as tk
from abc import ABCMeta, abstractmethod

from src.gui.widgets.resizing_font import ResizingFont


class ResizingFontTransparentWidget(tk.Widget, metaclass=ABCMeta):
    def __init__(self, parent, relwidth=.8, relheight=.8, minsize=4, maxsize=100, **kwargs):
        if kwargs.get('bg', None) in ('transparent', None):
            kwargs['bg'] = parent.cget('background')
            kwargs.setdefault('bd', 0)

        super().__init__(parent, **kwargs)

        base_font = kwargs.get('font', ('Comic Sans MS',))
        self._font = ResizingFont(self, self.get_text, base_font, relwidth,
                                  relheight, minsize, maxsize)
        self._font.resize_font()

        self._set_font(self._font)

    @abstractmethod
    def _set_font(self, font: ResizingFont): ...

    def get_text(self) -> str:
        return self.cget('text')

    def destroy(self):
        self._font.unbind()
        super().destroy()


class ResizingLabel(ResizingFontTransparentWidget, tk.Label):
    def _set_font(self, font: ResizingFont):
        self.config(font=font)


class ResizingButton(ResizingFontTransparentWidget, tk.Button):
    def _set_font(self, font: ResizingFont):
        self.config(font=font)
