import src.pypair as pp
from src.algorithms.tournament import Tournament, Result, Game, Round
from src.player import Player


class SwissTournament(Tournament):
    def __init__(self, name, players):
        super().__init__(name, players)
        self._engine = pp.Tournament()

    def _get_default_points(self) -> tuple:
        return 0, 0, 0

    def _get_win_draw_lost_points(self) -> tuple[int, int, int]:
        return 2, 1, 0

    def _pair_round(self) -> tuple[Round, list[Player]]:
        if not self.is_started():
            self.__add_players_to_engine()
        else:
            self.__report_engine_results()

        return self.__make_pairs()

    def __add_players_to_engine(self):
        for i, player in enumerate(self._players):
            self._engine.addPlayer(i, player.name)

    def __report_engine_results(self):
        for i, game in enumerate(self.active_round):
            if game.result == Result.White:
                self._engine.reportMatch(i + 1, (2, 0, 0))
            elif game.result == Result.Black:
                self._engine.reportMatch(i + 1, (0, 2, 0))
            elif game.result == Result.Draw:
                self._engine.reportMatch(i + 1, (1, 1, 0))
            else:
                raise Exception('Cannot report not ended game')

    def __make_pairs(self):
        pairs = self._engine.pairRound()

        round_ = []
        pause = self._players.copy()

        for _, (white_id, black_id) in pairs.items():
            round_.append(Game(self._players[white_id], self._players[black_id], Result.Playing))

            pause.remove(self._players[white_id])
            pause.remove(self._players[black_id])

        assert len(pause) <= 1, 'Cannot make pairs (too many pause)'
        assert len(round_) > 0, 'Cannot make pairs (zero games)'

        return round_, pause

    def _update_points(self):
        new_points = []

        for points, stats in zip(self._points, self._stats):
            win_op_points = sum(self._points[i][0] for i in stats[Result.White])
            draw_op_points = sum(self._points[i][0] for i in stats[Result.Draw])
            lost_op_points = sum(self._points[i][0] for i in stats[Result.Black])

            new_points.append((
                points[0],
                win_op_points * 3 + draw_op_points,
                lost_op_points
            ))

        self._points = new_points
