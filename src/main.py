import logging
import os

from src.config import Config
from src.gui.main_window import MainWindow


def main():
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(Config.LOG_TB_FILE), exist_ok=True)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.WARNING,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=Config.LOG_FILE)

    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)

    MainWindow().mainloop()

if __name__ == '__main__':
    main()
