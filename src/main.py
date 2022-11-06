import logging
import locale

from src.config import Config
from src.gui.main_window import MainWindow


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.WARNING,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=Config.LOG_FILE)

    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)

    locale.setlocale(locale.LC_TIME, 'PL_pl')

    MainWindow().mainloop()

if __name__ == '__main__':
    main()
