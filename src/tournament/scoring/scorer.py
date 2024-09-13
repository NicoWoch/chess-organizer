from abc import ABC, abstractmethod
from typing import Iterable

from src.tournament.round import Round
from src.tournament.round_stats import RoundStats

type Score = tuple[float, ...]


class Scorer(ABC):
    @abstractmethod
    def calculate_scores(self, no_players: int, rounds: list[Round], stats: RoundStats) -> tuple[Score, ...]: ...

    def create_scoreboard(self, no_players: int, rounds: list[Round], stats: RoundStats) -> tuple[tuple[int, int, Score], ...]:
        scores = self.calculate_scores(no_players, rounds, stats)
        scoreboard = list(enumerate(scores))
        scoreboard.sort(key=lambda x: (x[1], x[0]), reverse=True)
        places = self.__count_scoreboard_places(score for player, score in scoreboard)

        return tuple((place, player, score) for place, (player, score) in zip(places, scoreboard))

    @staticmethod
    def __count_scoreboard_places(scores: Iterable[Score]) -> list[int]:
        last_score = None
        place = -1
        places = []

        for def_place, score in enumerate(scores, start=1):
            if score != last_score:
                place = def_place

            places.append(place)
            last_score = score

        return places
