import logging
import tkinter as tk
import tkinter.ttk as ttk
from collections.abc import Callable

from src import db
from src.config import Config
from src.gui.subwindows.player_editor_window import PlayerEditorWindow
from src.player import Player, Gender
import src.gui.gui_utils as utils


class PlayerBrowserWindow(tk.Toplevel):
    def __init__(self, parent, add_to_tournament: Callable):
        super().__init__(parent)

        self.title('Wszyscy Gracze')
        self.geometry('+500+300')
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        self.__photos = []
        self.add_to_tournament = add_to_tournament
        self.players = db.get_players()
        self.treeview = None

        self.make_treeview()
        self.make_action_bar()

    def make_treeview(self):
        column_names = ('#', 'Imie', 'Nazwisko', 'Ranking')
        column_sizes = (20, 100, 100, 100)

        self.treeview = ttk.Treeview(self, columns=column_names, show='headings', height=10)

        for name, size in zip(column_names, column_sizes):
            self.treeview.heading(name, text=name, anchor=tk.CENTER)
            self.treeview.column(name, anchor=tk.CENTER, width=size)

        self.treeview.pack(fill='x')

        self.update_treeview()

    def update_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for i, player in enumerate(self.players):
            self.treeview.insert('', 'end', values=(i + 1, player.name, player.surname, player.rating))

        self.auto_save()

    def get_selection_gen(self):
        selected_players = self.treeview.selection()

        for player_id in selected_players:
            player_idx = self.treeview.item(player_id)['values'][0] - 1
            yield player_idx

    def make_action_bar(self):
        action_bar = utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.add_player_btn, tk.LEFT),
            utils.Action('minus.png', self.remove_players_btn, tk.LEFT),
            utils.Action('edit.png', self.edit_player, tk.LEFT),
            utils.Action('open.png', self.add_to_tournament_btn, tk.RIGHT),
        ], (40, 40))

        action_bar.pack(fill='x')

    def add_player_btn(self):
        new_player = Player.create_player(
            name='', surname='', gender=Gender.Men, rating=1000
        )

        def on_save():
            self.players.append(new_player)
            self.update_treeview()

        PlayerEditorWindow(self, new_player, on_save)

    def remove_players_btn(self):
        for player_idx in sorted(self.get_selection_gen(), reverse=True):
            del self.players[player_idx]

        self.update_treeview()

    def edit_player(self):
        selection = list(self.get_selection_gen())

        if len(selection) != 1:
            logging.warning('Cannot edit more/less than one player')
            return

        player = self.players[selection[0]]
        PlayerEditorWindow(self, player, self.update_treeview)

    def add_to_tournament_btn(self):
        selected_players = [self.players[idx] for idx in self.get_selection_gen()]
        self.add_to_tournament(selected_players)

    def auto_save(self):
        db.save_players(self.players)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    PlayerBrowserWindow(root, lambda x: print('Added:\n', '\n'.join(map(str, x)), sep=''))
    root.mainloop()
