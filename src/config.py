import os
from datetime import datetime


class Config:
    BASE_DIR = 'C:/Users/48502/PycharmProjects/chess-organizer'
    VERSION = 'V0.1'

    __log_file_time = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    LOG_FILE = os.path.join(BASE_DIR, 'logs', __log_file_time + '.log')
    LOG_TB_FILE = os.path.join(BASE_DIR, 'logs', __log_file_time + '.log-tb')

    WINDOW_NAME = f'Chess Organizer {VERSION}'
    WINDOW_ICON_PATH = os.path.join(BASE_DIR, 'src/images/icon.ico')
    WINDOW_SIZE = 1080, 640

    DB_PLAYERS = os.path.join(BASE_DIR, 'db/players.pickle')
    DB_TOURNAMENTS = os.path.join(BASE_DIR, 'db/tournaments.pickle')

    GUI_IMAGES_DIR = os.path.join(BASE_DIR, 'src/images')
