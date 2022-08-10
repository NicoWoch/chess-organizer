import random

from src.algorithms.tournament import Tournament
from src.algorithms.game import Round, Result, Game
from src.player import Player


class RandomTournament(Tournament):
    def _get_default_points(self) -> tuple:
        return 0,

    def _get_win_draw_lost_points(self) -> tuple[int, int, int]:
        return 2, 1, 0

    def _pair_round(self) -> tuple[Round, list[Player]]:
        players = self._players.copy()

        if len(self._players) % 2 == 1:  # Choose pause
            pause = [random.choice(players)]
            players.remove(pause[0])
        else:
            pause = []

        new_round = []
        while players:
            white = random.choice(players)
            players.remove(white)

            black = random.choice(players)
            players.remove(black)

            new_round.append(Game(white, black, Result.Playing))

        return new_round, pause

    def _update_points(self):
        return
