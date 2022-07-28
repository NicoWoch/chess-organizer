from dataclasses import dataclass
from typing import List, Optional

from swissdutch import constants
from swissdutch import dutch
from swissdutch import player as dutch_player

from src.player import Player

WHITE = 'WHITE'
BLACK = 'BLACK'
DRAW = 'DRAW'


@dataclass
class Game:
    white: Player
    black: Player
    who_win: Optional[str]


class SwissTournament:
    def __init__(self, players: List[Player]):
        self.players = players
        self.dutch_players = [dutch_player.Player(
            name=i,
            rating=p.rating,
        ) for i, p in enumerate(players)]

        self.rounds: List[List[Game]] = []
        self.pausing_players: List[Player] = []

        self.points = [(0, 0, 0) for _ in players]
        self.stats = [{'win': [], 'draw': [], 'lost': []} for _ in players]

    def _find_game(self, player: Player):
        for game in self.rounds[-1]:
            if game.white == player or game.black == player:
                return game

        raise ValueError('Game not found')

    def set_win(self, player: Player):
        game = self._find_game(player)

        if game.white == player:
            game.who_win = WHITE
        elif game.black == player:
            game.who_win = BLACK

    def set_draw(self, player: Player):
        game = self._find_game(player)
        game.who_win = DRAW

    def start_round(self):
        engine = dutch.DutchPairingEngine()
        new_players = engine.pair_round(len(self.rounds) + 1, self.dutch_players)
        new_players.sort(key=lambda x: x.rating)

        self.dutch_players = new_players.copy()

        self.rounds.append([])
        pause = None
        while new_players:
            player1 = new_players.pop()

            if player1.opponents[-1] == 0:
                pause = self.players[player1.name]
                continue

            player2 = next(p for p in new_players if p.pairing_no == player1.opponents[-1])
            new_players.remove(player2)

            if player1.colour_hist[-1] == constants.Colour.white:
                self.rounds[-1].append(Game(self.players[player1.name], self.players[player2.name], None))
            else:
                self.rounds[-1].append(Game(self.players[player2.name], self.players[player1.name], None))

        self.pausing_players.append(pause)

    def finish_round(self):
        new_points = []

        for player, points, stats in zip(self.players, self.points, self.stats):
            if player == self.pausing_players[-1]:
                won_points = 3
            else:
                game = self._find_game(player)

                has_won = (game.white == player and game.who_win == WHITE) or \
                          (game.black == player and game.who_win == BLACK)
                has_draw = game.who_win == DRAW

                won_points = 3 if has_won else (1 if has_draw else 0)

            win_points = sum(self.points[i][0] for i in stats['win'])
            draw_points = sum(self.points[i][0] for i in stats['draw'])
            lost_points = sum(self.points[i][0] for i in stats['lost'])

            new_points.append((
                points[0] + won_points,
                win_points * 3 + draw_points,
                lost_points
            ))

        self.points = new_points

    def get_scoreboard(self):
        pass

    def update_ratings(self):
        pass
