import logging
import tkinter as tk
from collections.abc import Callable

from src.db import MainDB
from src.gui.subwindows.browser_window import BrowserWindow
from src.gui.subwindows.tournament_creation_window import TournamentCreationWindow
import src.gui.gui_utils as utils


class TournamentBrowserWindow(BrowserWindow):
    def __init__(self, parent, open_tournament: Callable):
        super().__init__(parent)

        self.title('Wszystkie Turnieje')

        self.open_tournament = open_tournament
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
            if tournament.name in [t.name for t in self.tournaments]:
                raise Exception('That name is already occupied')

            self.tournaments.append(tournament)
            self.update_table()

        TournamentCreationWindow(self, on_create)

    def minus_btn(self):
        for player_idx in sorted(self.table.get_selected_ids(), reverse=True):
            del self.tournaments[player_idx]

        self.update_table()

    def open_btn(self):
        selected_ids = list(self.table.get_selected_ids())

        if len(selected_ids) > 1:
            logging.warning('More than one tournament selected')
            return
        elif len(selected_ids) == 0:
            logging.warning('No tournament is selected')
            return

        self.open_tournament(self.tournaments[selected_ids[0]])
        self.destroy()

    def auto_save(self):
        MainDB.save_tournaments(self.tournaments)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    TournamentBrowserWindow(root, lambda x: print('Opening tournament:', x.name))
    root.mainloop()
