import copy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Gender(Enum):
    Men = 'Mężczyzna'
    Women = 'Kobieta'
    Other = 'Inna'


@dataclass
class Player:
    _name: str
    _surname: str
    gender: Gender
    creation_date: datetime
    last_played: Optional[datetime]
    group_name: str

    _ratings_history: list[tuple[datetime, int]]

    @classmethod
    def create_player(cls, *, name: str, surname: str, gender: Gender, rating: int, group_name: str = ''):
        now = datetime.now().astimezone()
        return Player(
            name.title(), surname.title(), gender,
            now, None, group_name,
            [(now, rating)]
        )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value.title()

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value: str):
        self._surname = value.title()

    @property
    def rating(self) -> int:
        return self._ratings_history[-1][1]

    @rating.setter
    def rating(self, value: int):
        self._ratings_history.append((datetime.now().astimezone(), value))

    def change_group(self, group_name: str):
        self.group_name = group_name

    def trigger_playing(self):
        self.last_played = datetime.now().astimezone()

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name and self.surname == other.surname

    def __str__(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())


def sort_players_nice(players: list[Player]):
    players.sort(key=lambda p: (p.surname, p.name, p.creation_date))


def sorted_players_nice(players: list[Player]) -> list[Player]:
    lst = copy.deepcopy(players)
    sort_players_nice(lst)
    return lst
