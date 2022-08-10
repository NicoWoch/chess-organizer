import os
import tkinter as tk

from src.config import Config
import src.gui.gui_utils as utils


class LicenseWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Licencja')
        self.iconbitmap(Config.WINDOW_ICON_PATH)
        utils.center_window(self, (600, 500))

        license_file = open(os.path.join(Config.BASE_DIR, 'license.md'))

        license_text = tk.Text(self)
        license_text.insert('end', license_file.read())
        license_text.config(state=tk.DISABLED)
        license_text.place(x=0, y=0, relwidth=1, relheight=1)
