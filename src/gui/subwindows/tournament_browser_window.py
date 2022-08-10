import tkinter as tk
from collections.abc import Callable

import src.gui.gui_utils as utils
from src.config import Config
from src.db import MainDB
from src.gui.subwindows.browser_window import BrowserWindow
from src.gui.subwindows.info.confirm_window import confirm
from src.gui.subwindows.info.error_window import WindowException
from src.gui.subwindows.tournament_creation_window import TournamentCreationWindow


class TournamentBrowserWindow(BrowserWindow):
    def __init__(self, parent, open_tournament: Callable, close_tournament: Callable):
        super().__init__(parent)

        self.title('Wszystkie Turnieje')

        self.open_tournament = open_tournament
        self.close_tournament = close_tournament
        self.tournaments = MainDB.load_tournaments()

        self.table.set_columns(('#', 'Nazwa', 'Liczba Graczy'), (1, 10, 4))
        self.update_table()

    def make_action_bar(self):
        return utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.plus_btn, tk.LEFT),
            utils.Action('minus.png', self.minus_btn, tk.LEFT),
            utils.Action('open.png', self.open_btn, tk.RIGHT),
        ], (40, 40))

    def update_table(self):
        self.table.clear_rows()

        for i, tournament in enumerate(self.tournaments, start=1):
            self.table.add_row(i, tournament.name, len(tournament.players))

        self.auto_save()

    def plus_btn(self):
        def on_create(tournament):
            assert tournament.name not in [t.name for t in self.tournaments], WindowException(Config.ErrorMsg.TOURNAMENT_ALREADY_EXISTS)

            self.tournaments.append(tournament)
            self.update_table()

            self.open_tournament(tournament)
            self.destroy()

        TournamentCreationWindow(self, on_create)

    def minus_btn(self):
        assert len(self.table.get_selected_ids()) > 0, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_SELECTED_FOR_DELETION)

        tournament_count = len(self.table.get_selected_ids())
        if tournament_count == 1:
            tournament = self.tournaments[self.table.get_selected_ids()[0]]
            confirm(self, f'usunąć turniej {tournament.name}', self._remove_selected_tournaments)
        elif 1 < tournament_count < 5:
            confirm(self, f'usunąć {tournament_count} turnieje', self._remove_selected_tournaments)
        else:
            confirm(self, f'usunąć {tournament_count} turniejów', self._remove_selected_tournaments)

    def _remove_selected_tournaments(self):
        for player_idx in sorted(self.table.get_selected_ids(), reverse=True):
            del self.tournaments[player_idx]

        self.update_table()
        self.close_tournament()

    def open_btn(self):
        selected_ids = list(self.table.get_selected_ids())

        assert len(selected_ids) != 0, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_SELECTED_FOR_OPEN)
        assert len(selected_ids) == 1, WindowException(Config.ErrorMsg.MORE_THAN_ONE_TOURNAMENT_SELECTED)

        self.open_tournament(self.tournaments[selected_ids[0]])
        self.destroy()

    def auto_save(self):
        MainDB.save_tournaments(self.tournaments)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    TournamentBrowserWindow(root, lambda x: print('Opening tournament:', x.name), lambda: 0)
    root.mainloop()
