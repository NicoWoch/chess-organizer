import logging
import os.path
import pickle
from typing import List

from src.algorithms.tournament import Tournament
from src.config import Config
from src.player import Player


def get_players() -> List[Player]:
    if not os.path.exists(Config.DB_PLAYERS):
        logging.info(f'Creating players database in file "{Config.DB_PLAYERS}"')
        save_players([], no_debug=True)

    logging.info(f'Loading players from file "{Config.DB_PLAYERS}"')

    players = pickle.load(open(Config.DB_PLAYERS, 'rb'))
    assert isinstance(players, list), 'Importing Error (other instance)'
    assert len(players) == 0 or isinstance(players[0], Player), 'Importing Error (other instance in list)'
    return players


def save_players(players: List[Player], no_debug=False):
    if not no_debug:
        logging.info(f'Saving players to file "{Config.DB_PLAYERS}"')

    pickle.dump(players, open(Config.DB_PLAYERS, 'wb'))


def get_tournaments() -> List[Tournament]:
    if not os.path.exists(Config.DB_TOURNAMENTS):
        logging.info(f'Creating tournaments database in file "{Config.DB_PLAYERS}"')
        save_tournaments([], no_debug=True)

    logging.info(f'Loading tournaments from file "{Config.DB_TOURNAMENTS}"')

    tournaments = pickle.load(open(Config.DB_TOURNAMENTS, 'rb'))
    assert isinstance(tournaments, list), 'Importing Error (other instance)'
    assert len(tournaments) == 0 or isinstance(tournaments[0], Tournament), 'Importing Error (other instance in list)'
    return tournaments


def save_tournaments(tournaments: List[Tournament], no_debug=False):
    if not no_debug:
        logging.info(f'Saving tournaments to file "{Config.DB_TOURNAMENTS}"')

    pickle.dump(tournaments, open(Config.DB_TOURNAMENTS, 'wb'))
