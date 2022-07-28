import pickle
from enum import Enum, auto
from typing import List


class Gender(Enum):
    Men = auto()
    Women = auto()
    Other = auto()


class Player:
    def __init__(self, name: str, surname: str, gender: Gender, rating: int):
        self.name = name.title()
        self.surname = surname.title()
        self.gender = gender
        self.rating = rating

    def __eq__(self, other):
        return self.name == other.name and self.surname == other.surname

    def __str__(self):
        return f'<{self.name} {self.surname}>'

    def __repr__(self):
        return f"Player('{self.name}', '{self.surname}', {self.gender}, {self.rating})"


class PlayerList(list):
    def __init__(self, players: List[Player]):
        super().__init__(players)

    def save_players(self, filepath):
        pickle.dump(self, open(filepath, 'wb'))

    @staticmethod
    def load_players(filepath):
        player_list = pickle.load(open(filepath, 'rb'))
        assert isinstance(player_list, PlayerList)
        return player_list
