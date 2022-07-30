from typing import List
import random

from src.algorithms.tournament import Tournament, Round, Result, Game
from src.player import Player


class RandomTournament(Tournament):
    def __init__(self, name, players):
        super().__init__(name, players)

        self.rounds: List[Round] = []
        self.waiting_players: List[Player] = []

        self.points: List[int] = [0 for _ in players]

        self.next_round()

    def get_waiting_players(self, round_id=-1):
        return [self.waiting_players[round_id]]

    def get_rounds(self):
        return self.rounds

    def get_scoreboard(self):
        return sorted(zip(self.players, self.points), key=lambda x: x[1], reverse=True)

    def set_result(self, table_id, result):
        game = self.get_last_round()[table_id]
        game.result = result

        white_id = self.players.index(game.white)
        black_id = self.players.index(game.black)

        if game.result == Result.White:
            self.points[white_id] += 2
        elif game.result == Result.Black:
            self.points[black_id] += 2
        elif game.result == Result.Draw:
            self.points[white_id] += 1
            self.points[black_id] += 1
        else:
            raise ValueError('Bad result')

    def next_round(self):
        if len(self.rounds) != 0 and not self.has_round_ended():
            raise Exception('Round not ended yet')

        new_round = []
        players = self.players.copy()
        while players:
            white = random.choice(players)
            players.remove(white)

            black = random.choice(players)
            players.remove(black)

            new_round.append(Game(white, black, Result.Playing))

        print(new_round)
        self.rounds.append(new_round)

    def end_tournament(self):
        if not self.has_round_ended():
            raise Exception('Round not ended yet')
