import os
from os.path import dirname
from datetime import datetime


class Config:
    BASE_DIR = dirname(dirname(os.path.realpath(__file__)))
    VERSION = 'V0.3'

    __log_file_time = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    LOG_FILE = os.path.join(BASE_DIR, 'logs', __log_file_time + '.log')
    LOG_TB_FILE = os.path.join(BASE_DIR, 'logs', __log_file_time + '.log-tb')

    WINDOW_NAME = f'Chess Organizer {VERSION}'
    WINDOW_ICON_PATH = os.path.join(BASE_DIR, 'images/logo.ico')
    WINDOW_SIZE = 1080, 640

    DB_PLAYERS = os.path.join(BASE_DIR, 'db/players.pickle')
    DB_TOURNAMENTS = os.path.join(BASE_DIR, 'db/tournaments.pickle')

    GUI_IMAGES_DIR = os.path.join(BASE_DIR, 'images')

    ELO_K_VALUE = 20

    class ErrorMsg:
        TOURNAMENT_NOT_OPENED = 'Nie otwarto tunieju'
        TABLE_NOT_SELECTED = 'Nie wybrano stołu'
        CANNOT_EDIT_IN_CLOSED_ROUND = 'Nie można edytować wyników w zamkniętej rundzie'
        TOO_LESS_PLAYERS_IN_TOURNAMENT = 'Zbyt mała ilość graczy w turnieju.\nProszę dodać przynajmniej dwóch graczy'
        TOURNAMENT_HAS_ENDED = 'Turniej jest zakończony'
        NOT_ALL_GAMES_ENDED = 'Nie na wszystkich stołach zakończyły się partie.\nProszę dodaj brakujące wyniki i spróbuj ponownie'
        CANNOT_PAIR = 'Nie można utworzyć par.\nNajczęściej oznacza to że należy zakończyć turniej'
        TOURNAMENT_NOT_STARTED = 'Turniej nie został rozpoczęty'

        PLAYER_NOT_FOUND = 'Program nie znalazł graczy:\n\n{players}\n\n' \
                           'Oznacza to że zostali oni usunięci i program\nnie będzie aktualizował ich rankingów'
        PLAYER_ALREADY_ADDED = 'Gracze:\n\n{players}\n\n' \
                               'Zostali już wcześniej dodani do turnieju'

        CANNOT_ADD_PLAYER_WHEN_STARTED = 'Nie można dodać graczy kiedy\nturniej jest rozpoczęty lub zakończony'
        CANNOT_REMOVE_PLAYER_WHEN_STARTED = 'Nie można usunąć graczy kiedy\nturniej jest rozpoczęty lub zakończony'
        PLAYER_NOT_SELECTED = 'Nie wybrano gracza'

        TOURNAMENT_ALREADY_EXISTS = 'Ta nazwa jest już zajęta.\nWybierz inną'
        # TOURNAMENT_NOT_SELECTED_FOR_DELETION = 'Nie wybrano turnieju do usunięcia'
        MORE_THAN_ONE_TOURNAMENT_SELECTED = 'Wybrano więcej niż jeden turniej do otwarcia'
        TOURNAMENT_NOT_SELECTED_FOR_OPEN = 'Nie wybrano turnieju do otwarcia'

        PLAYER_ALREADY_EXISTS = 'Ten gracz już istnieje'
        # PLAYER_NOT_SELECTED_FOR_DELETION = 'Nie wybrano gracza do usunięcia'
        # MORE_THAN_ONE_PLAYER_SELECTED = 'Wybrano więcej niż jednego gracza'
        # PLAYER_NOT_SELECTED_FOR_EDIT = 'Nie wybrano gracza do edycji'
        PLAYER_NOT_SELECTED_FOR_OPEN = 'Nie wybrano gracza do dodania'
