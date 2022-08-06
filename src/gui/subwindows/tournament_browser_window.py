import logging
import tkinter as tk
import tkinter.ttk as ttk
from collections.abc import Callable

from src import db
from src.config import Config
from src.gui.subwindows.tournament_creation_window import TournamentCreationWindow
import src.gui.gui_utils as utils


class TournamentBrowserWindow(tk.Toplevel):
    def __init__(self, parent, open_tournament: Callable):
        super().__init__(parent)

        self.title('Wszystkie Turnieje')
        self.geometry('+500+300')
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        self.open_tournament = open_tournament
        self.__photos = []
        self.tournaments = db.get_tournaments()
        self.treeview = None

        self.make_treeview()
        self.make_action_bar()

    def make_treeview(self):
        column_names = ('#', 'Nazwa', 'Liczba Graczy')
        column_sizes = (20, 200, 80)

        self.treeview = ttk.Treeview(self, columns=column_names, show='headings', height=10)

        for name, size in zip(column_names, column_sizes):
            self.treeview.heading(name, text=name, anchor=tk.CENTER)
            self.treeview.column(name, anchor=tk.CENTER, width=size)

        self.treeview.pack(fill='x')

        self.update_treeview()

    def update_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for i, tournament in enumerate(self.tournaments):
            self.treeview.insert('', 'end', values=(i + 1, tournament.name, len(tournament.players)))

        self.auto_save()

    def get_selection_gen(self):
        selected_players = self.treeview.selection()

        for player_id in selected_players:
            player_idx = self.treeview.item(player_id)['values'][0] - 1
            yield player_idx

    def make_action_bar(self):
        action_bar = utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.add_tournament_btn, tk.LEFT),
            utils.Action('minus.png', self.remove_tournament_btn, tk.LEFT),
            utils.Action('open.png', self.open_tournament_btn, tk.RIGHT),
        ], (40, 40))

        action_bar.pack(fill='x')

    def add_tournament_btn(self):
        def on_create(tournament):
            if tournament.name in [t.name for t in self.tournaments]:
                raise Exception('That name is already occupied')

            self.tournaments.append(tournament)
            self.update_treeview()

        TournamentCreationWindow(self, on_create)

    def remove_tournament_btn(self):
        for player_idx in sorted(self.get_selection_gen(), reverse=True):
            del self.tournaments[player_idx]

        self.update_treeview()

    def open_tournament_btn(self):
        selected_ids = list(self.get_selection_gen())

        if len(selected_ids) > 1:
            logging.warning('More than one tournament selected')
            return
        elif len(selected_ids) == 0:
            logging.warning('No tournament is selected')
            return

        self.open_tournament(self.tournaments[selected_ids[0]])
        self.destroy()

    def auto_save(self):
        db.save_tournaments(self.tournaments)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    TournamentBrowserWindow(root, lambda x: print('Opening tournament:', x.name))
    root.mainloop()
