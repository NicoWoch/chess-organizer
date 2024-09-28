import tkinter as tk
from typing import Callable

from src.gui.widgets.table_frame import TableFrame
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.round import Round, GameResult

SWAP_IMG = '../resources/swap_arrows.png'
REMOVE_BTN = '../resources/remove_btn.png'


class PairingEditor(tk.Toplevel):
    def __init__(self, parent, tournament: InteractiveTournament, change_round: Callable[[Round], None]):
        super().__init__(parent)

        self._players = tournament.players
        self._pause_count = tournament.stats.paused

        self._pairs = list(tournament.get_round().pairs)
        self._results = list(tournament.get_round().results)
        self._change_round = change_round

        self._images = []

        self.__define_layout()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()

        round_ = Round(len(self._players), tuple(self._pairs))

        for table, result in enumerate(self._results):
            round_.set_result(table, result)

        self._change_round(round_)

    def __define_layout(self):
        self.geometry("900x500")
        self.title("Pairing Editor")

        pairs_table_frame = tk.Frame(self, highlightbackground='black', highlightthickness=1)
        self.pairs_table = TableFrame(pairs_table_frame)

        pause_table_frame = tk.Frame(self, highlightbackground='black', highlightthickness=1)
        self.pause_table = TableFrame(pause_table_frame, table_settings={
            'selectable': True
        })

        self.__generate_pairs_table()
        self.__generate_pause_table()

        add_pair_btn = tk.Button(self, text='Add Pair', command=self._add_pair_from_selection)

        pairs_table_frame.place(x=0, y=0, relwidth=.65, relheight=1)
        pause_table_frame.place(anchor=tk.NE, relx=1, y=0, relwidth=.35, relheight=1)
        add_pair_btn.place(anchor=tk.SE, relx=1, rely=1, width=100, height=64)
        self.pairs_table.pack(side=tk.TOP, fill=tk.X)
        self.pause_table.pack(side=tk.TOP, fill=tk.X)

    def _refresh_tables(self):
        self.__generate_pairs_table()
        self.__generate_pause_table()

    def __generate_pairs_table(self):
        self._images = []

        headers = ['#', 'Biały', '', 'Czarny', '']
        rows = [
            [
                i + 1,
                self.__parse_player_id(pair[0]),
                self.__make_swap_btn(i),
                self.__parse_player_id(pair[1]),
                self.__make_remove_btn(i),
            ]
            for i, pair in enumerate(self._pairs)
        ]

        self.pairs_table.set_data([headers] + rows)
        self.pairs_table.columns_weights = [1, 20, 1, 20, 1]

    def __parse_player_id(self, player_id: int) -> str:
        player = self._players[player_id]
        return player.name

    def __make_swap_btn(self, index: int):
        img = tk.PhotoImage(file=SWAP_IMG).subsample(3, 3)
        self._images.append(img)
        command = lambda i=index: self.swap_pair(i)
        return tk.Button(self.pairs_table.container, text=index, image=img, width=2, height=2, command=command)

    def __make_remove_btn(self, index: int):
        img = tk.PhotoImage(file=REMOVE_BTN)
        self._images.append(img)
        command = lambda i=index: self.remove_pair(i)
        return tk.Button(self.pairs_table.container, text=index, image=img, width=2, height=2, command=command)

    def __generate_pause_table(self):
        headers = ['#', 'Gracz', 'Pauzy']
        paused_players = [pid for pid, _ in enumerate(self._players) if all(pid not in pair for pair in self._pairs)]
        rows = [
            [
                player_id + 1,
                self.__parse_player_id(player_id),
                self._pause_count[player_id]
            ]
            for player_id in paused_players
        ]

        self.pause_table.set_data([headers] + rows)
        self.pause_table.columns_weights = [1, 20, 1]

    def _add_pair_from_selection(self):
        selection = self.pause_table.get_selection()

        if len(selection) != 2:
            return

        sa, sb = tuple(selection)
        self.add_pair(self.pause_table.get_data()[sa][0] - 1, self.pause_table.get_data()[sb][0] - 1)
        self.pause_table.clear_selection()

    def swap_pair(self, table_id: int):
        swap_pair = lambda p: (p[1], p[0])

        self._pairs[table_id] = swap_pair(self._pairs[table_id])
        game_result_swap = {
            GameResult.WIN: GameResult.LOSE,
            GameResult.LOSE: GameResult.WIN,
            GameResult.PLAYER_A_NOT_SHOWED_IN_TIME: GameResult.PLAYER_B_NOT_SHOWED_IN_TIME,
            GameResult.PLAYER_B_NOT_SHOWED_IN_TIME: GameResult.PLAYER_A_NOT_SHOWED_IN_TIME,
        }

        if self._results[table_id] in game_result_swap:
            self._results[table_id] = game_result_swap[self._results[table_id]]

        self._refresh_tables()

    def remove_pair(self, table_id: int):
        self._pairs.pop(table_id)
        self._results.pop(table_id)
        self._refresh_tables()

    def add_pair(self, player_a: int, player_b: int):
        self._pairs.append((player_a, player_b))
        self._results.append(None)
        self._refresh_tables()
