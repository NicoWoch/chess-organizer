import logging

from src.gui.main_window import MainWindow


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)


if __name__ == '__main__':
    MainWindow().mainloop()
