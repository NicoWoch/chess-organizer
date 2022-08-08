import logging
import tkinter as tk
from collections.abc import Callable
from copy import copy

from src.db import MainDB
from src.gui.subwindows.browser_window import BrowserWindow
from src.gui.subwindows.player_editor_window import PlayerEditorWindow
from src.player import Player, Gender
import src.gui.gui_utils as utils


class PlayerBrowserWindow(BrowserWindow):
    def __init__(self, parent, add_to_tournament: Callable):
        super().__init__(parent)

        self.title('Wszyscy gracze')

        self.add_to_tournament = add_to_tournament
        self.players = MainDB.load_players()

        self.table.set_columns(('#', 'Imie', 'Nazwisko', 'Ranking'), (1, 5, 5, 5))
        self.update_table()

    def make_action_bar(self):
        return utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.plus_btn, tk.LEFT),
            utils.Action('minus.png', self.minus_btn, tk.LEFT),
            utils.Action('edit.png', self.edit_btn, tk.LEFT),
            utils.Action('open.png', self.open_btn, tk.RIGHT),
        ], (40, 40))

    def update_table(self):
        self.table.clear_rows()

        for i, player in enumerate(self.players, start=1):
            self.table.add_row(i, player.name, player.surname, player.rating)

        self.auto_save()

    def plus_btn(self):
        new_player = Player.create_player(
            name='', surname='', gender=Gender.Men, rating=1000
        )

        def on_save():
            if new_player not in self.players:
                self.players.append(new_player)
                self.update_table()
            else:
                logging.error('The same player already exists')

        PlayerEditorWindow(self, new_player, on_save)

    def minus_btn(self):
        for player_idx in sorted(self.table.get_selected_ids(), reverse=True):
            del self.players[player_idx]

        self.update_table()

    def edit_btn(self):
        selection = list(self.table.get_selected_ids())

        if len(selection) != 1:
            logging.warning('Cannot edit more/less than one player')
            return

        player_copy = copy(self.players[selection[0]])

        def on_save():
            if player_copy not in self.players:
                self.players[selection[0]] = player_copy
                self.update_table()
            else:
                logging.error('The same player already exists')

        PlayerEditorWindow(self, player_copy, on_save)

    def open_btn(self):
        selected_players = [self.players[idx] for idx in self.table.get_selected_ids()]
        self.add_to_tournament(selected_players)

    def auto_save(self):
        MainDB.save_players(self.players)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    PlayerBrowserWindow(root, lambda x: print('Added:\n', '\n'.join(map(str, x)), sep=''))
    root.mainloop()
