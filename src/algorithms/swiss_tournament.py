from typing import List

import src.pypair as pp
from src.algorithms.tournament import Tournament, Result, Game
from src.player import Player


class SwissTournament(Tournament):
    def __init__(self, players):
        self.players = players

        self.rounds: List[List[Game]] = []
        self.pausing_players: List[Player] = []

        self.swiss_engine = pp.Tournament()

        self.points = [(0, 0, 0) for _ in players]
        self.stats = [{'win': [], 'draw': [], 'lost': []} for _ in players]

        self._add_players_to_engine()
        self._start_round()

    def _add_players_to_engine(self):
        for i, player in enumerate(self.players):
            self.swiss_engine.addPlayer(i, player.name)

    def _start_round(self):
        pairs = self.swiss_engine.pairRound()

        self.rounds.append([])
        pause = self.players.copy()

        for table_id, (white_id, black_id) in pairs.items():
            self.rounds[-1].append(Game(self.players[white_id], self.players[black_id], Result.Playing))
            pause.remove(self.players[white_id])
            pause.remove(self.players[black_id])

        assert len(pause) <= 1

        self.pausing_players.append(pause[0] if pause else None)

    def _find_game(self, player: Player):
        for game in self.rounds[-1]:
            if game.white == player or game.black == player:
                return game

        raise ValueError('Game not found')

    def _update_small_points(self):
        new_points = []

        for player, points, stats in zip(self.players, self.points, self.stats):
            win_op_points = sum(self.points[i][0] for i in stats['win'])
            draw_op_points = sum(self.points[i][0] for i in stats['draw'])
            lost_op_points = sum(self.points[i][0] for i in stats['lost'])

            new_points.append((
                points[0],
                win_op_points * 3 + draw_op_points,
                lost_op_points
            ))

        self.points = new_points

    def get_players(self):
        return self.players

    def get_waiting_players(self, round_id=-1):
        return [self.pausing_players[round_id]]

    def get_rounds(self):
        return self.rounds

    def get_scoreboard(self):
        return sorted(zip(self.players, self.points), key=lambda x: x[1], reverse=True)

    def set_result(self, table_id, result):
        game = self.get_last_round()[table_id]
        game.result = result

        white_id = self.players.index(game.white)
        black_id = self.players.index(game.black)

        if result == Result.White:
            ws, bs = 'win', 'lost'
            p = [2, 0]
        elif result == Result.Black:
            ws, bs = 'lost', 'win'
            p = [0, 2]
        elif result == Result.Draw:
            ws, bs = 'draw', 'draw'
            p = [1, 1]
        else:
            raise ValueError('Bad result')

        self.stats[white_id][ws].append(black_id)
        self.stats[black_id][bs].append(white_id)

        self.points[white_id] = (self.points[white_id][0] + p[0], self.points[white_id][1], self.points[white_id][2])
        self.points[black_id] = (self.points[black_id][0] + p[1], self.points[black_id][1], self.points[black_id][2])

        self.swiss_engine.reportMatch(table_id + 1, p + [0])

    def next_round(self):
        if not self.has_round_ended():
            raise Exception('Round not ended yet')

        self._update_small_points()
        self._start_round()

    def end_tournament(self):
        if not self.has_round_ended():
            raise Exception('Round not ended yet')

        self._update_small_points()
