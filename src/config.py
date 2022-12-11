import os.path
from datetime import datetime


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    VERSION = 'V0.4'

    WINDOW_NAME = f'Chess Organizer {VERSION}'
    WINDOW_ICON_PATH = os.path.join(BASE_DIR, 'data/images/logo.ico')
    WINDOW_SIZE = 1080, 640

    LOG_DIR = os.path.join(BASE_DIR, 'data/logs')
    DB_DIR = os.path.join(BASE_DIR, 'data/db')
    IMAGES_DIR = os.path.join(BASE_DIR, 'data/images')
    TEMP_DIR = os.path.join(BASE_DIR, 'data/temp')

    DB_PLAYERS = os.path.join(DB_DIR, 'players.pkl')
    DB_TOURNAMENTS = os.path.join(DB_DIR, 'tournaments.pkl')
    LOG_FILE = os.path.join(LOG_DIR, datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log')

    ELO_K_VALUE = 20
    WIN_POINTS = 1
    DRAW_POINTS = .5
    LOSE_POINTS = 0
    PAUSE_POINTS = 1

    class ErrorMsg:
        TOURNAMENT_NOT_OPENED = 'Nie otwarto tunieju'
        TOURNAMENT_NOT_STARTED = 'Turniej nie został rozpoczęty'
        TOURNAMENT_HAS_ENDED = 'Turniej jest zakończony'
        TOURNAMENT_STARTED = 'Turniej jest już rozpoczęty'
        ROUND_NOT_ENDED = 'Nie na wszystkich stołach zakończyły się partie.\nProszę dodaj brakujące wyniki i spróbuj ponownie'


        CANNOT_EDIT_IN_CLOSED_ROUND = 'Nie można edytować wyników w zamkniętej rundzie'
        TOO_LESS_PLAYERS_IN_TOURNAMENT = 'Zbyt mała ilość graczy w turnieju.\nProszę dodać przynajmniej dwóch graczy'
        CANNOT_PAIR = 'Nie można utworzyć par.\nNajczęściej oznacza to że należy zakończyć turniej'

        PLAYER_NOT_FOUND = 'Program nie znalazł graczy:\n\n{players}\n\n' \
                           'Oznacza to że zostali oni usunięci i program\nnie będzie aktualizował ich rankingów'
        PLAYER_ALREADY_ADDED = 'Gracze:\n\n{players}\n\n' \
                               'Zostali już wcześniej dodani do turnieju'

        PLAYER_NOT_SELECTED = 'Nie wybrano gracza'

        TOURNAMENT_ALREADY_EXISTS = 'Ta nazwa jest już zajęta.\nWybierz inną'
        TOURNAMENT_NOT_SELECTED_FOR_OPEN = 'Nie wybrano turnieju do otwarcia'

        PLAYER_ALREADY_EXISTS = 'Ten gracz już istnieje'

        NOT_ON_PAGE_WITH_PAIRS = 'Brak wybranej rundy.\nProszę wybierz rundę i spróbuj ponownie'
        PLAYER_IMPORTING_ERROR = 'Błąd importowania graczy.\nNiepoprawny plik'
