import logging

from src.config import Config
from src.gui.main_window import MainWindow


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=Config.LOG_FILE)

logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)


if __name__ == '__main__':
    MainWindow().mainloop()
