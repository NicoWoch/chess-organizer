from tkinter import font as tkfont

DELTA_FONT_SIZE_CHANGE = .5


class ResizingFont(tkfont.Font):
    def __init__(self, parent, get_text, font=('Comic Sans MS',), relwidth=.8, relheight=.8, minsize=4, maxsize=100):
        super().__init__(font=font)

        self.parent = parent
        self.get_text = get_text
        self.relwidth = relwidth
        self.relheight = relheight
        self.minsize = minsize
        self.maxsize = maxsize

        self.__prev_height = 0

        self.bind_id = self.parent.bind('<Configure>', self.resize_font, add='+')

    def unbind(self):
        self.parent.unbind('<Configure>', self.bind_id)

    def resize_font(self, *_):
        self.config(size=self._calc_height())

    def _calc_height(self) -> int:
        text = self.get_text()

        if text == '':
            return 20

        text_height = self.cget('size')
        text_width = self.__measure_with_new_lines(text)

        requested_width = self.parent.winfo_width() * self.relwidth
        requested_height = self.parent.winfo_height() * self.relheight

        new_height_from_width = text_height * requested_width / text_width

        new_height = min(new_height_from_width, requested_height)
        new_height = max(min(new_height, self.maxsize), self.minsize)

        if self.__prev_height - DELTA_FONT_SIZE_CHANGE < new_height < self.__prev_height + DELTA_FONT_SIZE_CHANGE:
            return round(self.__prev_height)

        self.__prev_height = new_height

        return round(new_height)

    def __measure_with_new_lines(self, text: str):
        return max(self.measure(line) for line in text.splitlines())
