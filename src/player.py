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
    name: str
    surname: str
    gender: Gender
    title: str
    creation_date: datetime
    last_played: Optional[datetime]
    group_name: str

    _ratings_history: list[tuple[datetime, int]]
    _tournament_ids: list[int]

    def __post_init__(self):
        self.name = self.name.title()
        self.surname = self.surname.title()

    @classmethod
    def create_player(cls, *, name: str, surname: str, gender: Gender, rating: int, title: str = '', group_name: str = ''):
        now = datetime.now().astimezone()
        return Player(
            name, surname, gender, title,
            now, None, group_name,
            [(now, rating)], []
        )

    @property
    def rating(self) -> int:
        return self._ratings_history[-1][1]

    @rating.setter
    def rating(self, value: int):
        self._ratings_history.append((datetime.now().astimezone(), value))

    def add_tournament(self, tournament_id: int):
        self._tournament_ids.append(tournament_id)

    def change_group(self, group_name: str):
        self.group_name = group_name

    def trigger_playing(self):
        self.last_played = datetime.now().astimezone()

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name and self.surname == other.surname

    def __str__(self):
        return f'{self.name} {self.surname}'
