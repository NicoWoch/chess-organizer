import logging
import os.path
import pickle
from typing import Optional, Any

from src.algorithms.tournament import Tournament
from src.config import Config
from src.player import Player


class DB:
    def __init__(self):
        self.players_cache: Optional[list[Player]] = None
        self.tournaments_cache: Optional[list[Tournament]] = None

    def _load_object(self, filepath: str, default: Any) -> Any:
        if not os.path.exists(filepath):
            logging.debug(f'Creating file "{filepath}"')
            self._save_object(filepath, default)

        logging.debug(f'Loading object from file "{filepath}"')

        try:
            file = open(filepath, 'rb')
            return pickle.load(file)
        except OSError:
            logging.critical(f'Cannot open file "{filepath}" in "rb" mode')
            raise

    @classmethod
    def _save_object(cls, filepath: str, obj: Any):
        logging.debug(f'Saving object to file "{filepath}"')

        try:
            file = open(filepath, 'wb')
            pickle.dump(obj, file)
        except OSError:
            logging.critical(f'Cannot open file "{filepath}" in "wb" mode')
            raise

    @classmethod
    def _test_players(cls, players):
        assert isinstance(players, list), f'Players Testing Error ({type(players)=} != list)'
        if len(players) != 0:
            assert isinstance(players[0], Player), f'Players Testing Error ({type(players[0])=} != Player)'

    @classmethod
    def _test_tournaments(cls, tournaments):
        assert isinstance(tournaments, list), f'Tournaments Testing Error ({type(tournaments)=} != list)'
        if len(tournaments) != 0:
            assert isinstance(tournaments[0], Tournament), \
                f'Tournaments Testing Error ({type(tournaments[0])=} != Tournament)'

    def load_players(self, path=None) -> list[Player]:
        if path is None:
            path = Config.DB_PLAYERS

        if self.players_cache is not None and path == Config.DB_PLAYERS:
            logging.debug('Loading players from cache')
            return self.players_cache

        players = self._load_object(path, [])
        self._test_players(players)
        players = self._sort_players(players)

        if path == Config.DB_PLAYERS:
            self.players_cache = players

        return players

    def save_players(self, players: list[Player], path=None):
        if path is None:
            path = Config.DB_PLAYERS

        self._test_players(players)

        players = self._sort_players(players)
        self._save_object(path, players)

        if path == Config.DB_PLAYERS:
            self.players_cache = players

    @classmethod
    def _sort_players(cls, players: list[Player]) -> list[Player]:
        return sorted(players, key=lambda p: (p.surname, p.name, p.creation_date))

    def load_tournaments(self) -> list[Tournament]:
        if self.tournaments_cache is not None:
            logging.debug('Loading tournaments from cache')
            return self.tournaments_cache

        tournaments = self._load_object(Config.DB_TOURNAMENTS, [])
        self._test_tournaments(tournaments)
        self.tournaments_cache = tournaments
        return tournaments

    def save_tournaments(self, tournaments: list[Tournament]):
        self._test_tournaments(tournaments)
        self.tournaments_cache = tournaments
        self._save_object(Config.DB_TOURNAMENTS, tournaments)


MainDB = DB()
