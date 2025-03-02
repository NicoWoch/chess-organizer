import logging
import locale
import os
from typing import Iterable

from src.config import Config
from src.gui.main_window import MainWindow


def iter_logs() -> Iterable[str]:
    for path, directories, files in os.walk(Config.LOG_DIR):
        yield from [
            os.path.join(path, file)
            for file in files if Config.LOG_FILE_REGEX.match(file)
        ]


def log_clear():
    for path in iter_logs():
        if os.path.getsize(path) == 0:
            os.remove(path)


def main():
    log_clear()

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.WARNING,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=Config.LOG_FILE)

    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)

    locale.setlocale(locale.LC_TIME, '')

    MainWindow().mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.fatal('Fatal Exception!')
        logging.fatal(e)
        raise e
