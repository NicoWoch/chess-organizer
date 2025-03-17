import logging
import locale
import os
from typing import Iterable

from src.config import Config
from src.gui.main_window import MainWindow
from pathlib import Path


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
    # log_clear()  # ONLY FOR DEVELOPMENT

    Path(Config.USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(Config.LOG_DIR).mkdir(exist_ok=True)
    Path(Config.DB_DIR).mkdir(exist_ok=True)
    Path(Config.TEMP_DIR).mkdir(exist_ok=True)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.WARNING,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=Config.LOG_FILE,
        encoding='utf-8')

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
