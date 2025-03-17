from src.algorithms.constants import Round, Game, Result
from src.player import Player


class Tops:
    def __init__(self, scoreboard: list[Player], white_hists: list[int]):
        assert len(scoreboard) in (2, 4, 8), f'Cannot make tops from {len(scoreboard)} players'

        self.players = scoreboard
        self.rounds: list[Round] = []
        self.white_hists = white_hists

        self._generate_empty_rounds(len(self.players))
        self._fill_first_round()

    def _generate_empty_rounds(self, players_count: int):
        if players_count == 1:
            return

        self.rounds.append([Game(None, None, None) for _ in range(players_count // 2)])  # TODO: fix
        self._generate_empty_rounds(players_count // 2)

    def _fill_first_round(self):
        itr = iter(self.players)
        for i, (player_a, player_b) in enumerate(zip(itr, itr)):
            wh_a = self.white_hists[i * 2]
            wh_b = self.white_hists[i * 2 + 1]

            if wh_a < wh_b:
                self.rounds[0][i].white = player_a
                self.rounds[0][i].black = player_b
            else:
                self.rounds[0][i].white = player_b
                self.rounds[0][i].black = player_a

    def set_result(self, round_id: int, table_id: int, result: Result):
        raise NotImplementedError
