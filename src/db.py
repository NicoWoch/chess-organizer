import logging
import os.path
import pickle

from src.algorithms.tournament import Tournament
from src.config import Config
from src.player import Player


def get_players(*, debug=True) -> list[Player]:
    if not os.path.exists(Config.DB_PLAYERS):
        logging.info(f'Creating players database in file "{Config.DB_PLAYERS}"')
        save_players([], debug=False)

    if debug:
        logging.info(f'Loading players from file "{Config.DB_PLAYERS}"')

    players = pickle.load(open(Config.DB_PLAYERS, 'rb'))
    assert isinstance(players, list), 'Importing Error (other instance)'
    assert len(players) == 0 or isinstance(players[0], Player), 'Importing Error (other instance in list)'
    return players


def save_players(players: list[Player], *, debug=True):
    if debug:
        logging.info(f'Saving players to file "{Config.DB_PLAYERS}"')

    os.makedirs(os.path.dirname(Config.DB_PLAYERS), exist_ok=True)
    pickle.dump(players, open(Config.DB_PLAYERS, 'wb'))


def get_tournaments(*, debug=True) -> list[Tournament]:
    if not os.path.exists(Config.DB_TOURNAMENTS):
        logging.info(f'Creating tournaments database in file "{Config.DB_PLAYERS}"')
        save_tournaments([], debug=False)

    if debug:
        logging.info(f'Loading tournaments from file "{Config.DB_TOURNAMENTS}"')

    tournaments = pickle.load(open(Config.DB_TOURNAMENTS, 'rb'))
    assert isinstance(tournaments, list), 'Importing Error (other instance)'
    assert len(tournaments) == 0 or isinstance(tournaments[0], Tournament), 'Importing Error (other instance in list)'
    return tournaments


def save_tournaments(tournaments: list[Tournament], *, debug=True):
    if debug:
        logging.info(f'Saving tournaments to file "{Config.DB_TOURNAMENTS}"')

    os.makedirs(os.path.dirname(Config.DB_TOURNAMENTS), exist_ok=True)
    pickle.dump(tournaments, open(Config.DB_TOURNAMENTS, 'wb'))
