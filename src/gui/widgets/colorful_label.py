import tkinter as tk
import re


class ColorfulLabel(tk.Text):
    def __init__(self, parent, initial_text: str = '', **kwargs):
        super().__init__(parent, **kwargs)

        self._fgs = {}
        self._bgs = {}

        self.insert('end', initial_text)

        self.tag_configure('center', justify='center')
        self.tag_add('center', '1.0', 'end')

        self.configure(state='disabled', borderwidth=0, cursor='arrow')

    def colorize_range(self, start: int, end: int, fg: str, bg: str = None):
        if fg not in self._fgs:
            self.tag_configure(f'color_{fg}', foreground=fg)
            self._fgs[fg] = f'color_{fg}'

        if bg is not None and bg not in self._bgs:
            self.tag_configure(f'color_bg_{bg}', background=bg)
            self._bgs[bg] = f'color_bg_{bg}'

        self.tag_add(self._fgs[fg], f'1.{start}', f'1.{end}')

        if bg is not None:
            self.tag_add(self._bgs[bg], f'1.{start}', f'1.{end}')

    def colorize_regex(self, regex: re.Pattern | str, fg: str, bg: str = None):
        if not isinstance(regex, re.Pattern):
            regex = re.compile(regex)

        for match in regex.finditer(self.get('1.0', 'end')):
            if match.group() == '':
                continue

            if match.lastindex is None:
                continue

            for group_i in range(1, match.lastindex + 1):
                self.colorize_range(*match.span(group_i), fg=fg, bg=bg)
