import logging
import os.path
import pickle
from typing import List

from src.algorithms.tournament import Tournament
from src.player import Player

BASE_DIR = 'C:/Users/48502/PycharmProjects/chess-organizer/src'
PLAYERS_DB = os.path.join(BASE_DIR, '../db/players.pickle')
TOURNAMENTS_DB = os.path.join(BASE_DIR, '../db/tournaments.pickle')


def get_players() -> List[Player]:
    logging.info(f'Loading players from file "{PLAYERS_DB}"')

    players = pickle.load(open(PLAYERS_DB, 'rb'))
    assert isinstance(players, list), 'Importing Error'
    assert len(players) == 0 or isinstance(players[0], Player), 'Importing Error'
    return players


def save_players(players: List[Player]):
    logging.info(f'Saving players to file "{PLAYERS_DB}"')

    pickle.dump(players, open(PLAYERS_DB, 'wb'))


def get_tournaments() -> List[Tournament]:
    logging.info(f'Loading tournaments from file "{TOURNAMENTS_DB}"')

    tournaments = pickle.load(open(TOURNAMENTS_DB, 'rb'))
    assert isinstance(tournaments, list), 'Importing Error'
    assert len(tournaments) == 0 or isinstance(tournaments[0], Tournament), 'Importing Error'
    return tournaments


def save_tournaments(tournaments: List[Tournament]):
    logging.info(f'Saving tournaments to file "{TOURNAMENTS_DB}"')

    pickle.dump(tournaments, open(TOURNAMENTS_DB, 'wb'))
