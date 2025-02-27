import tkinter as tk
from collections.abc import Callable
from copy import copy
from pickle import UnpicklingError
from tkinter.filedialog import asksaveasfilename, askopenfilename
from typing import Any

from src.config import Config
from src.db import MainDB
from src.gui import utils
from src.gui.subwindows.browser_window import BrowserWindow
from src.gui.subwindows.info.confirm_window import confirm
from src.gui.subwindows.info.error_window import WindowException
from src.gui.subwindows.player_editor_window import PlayerEditorWindow
from src.player import Player, Gender

EXPORT_IMPORT_FILE_EXT = [('Wszystkie Pliki', '*.*'),
                          ('Gracze', '*.players')]


class PlayerBrowserWindow(BrowserWindow):
    def __init__(self, parent, add_to_tournament: Callable):
        super().__init__(parent)

        self.title('Wszyscy gracze')
        utils.add_icon(self)
        utils.center_window(self, (550, 550))
        self.minsize(450, 100)

        self.add_to_tournament = add_to_tournament
        self.players = MainDB.load_players()

        self.update_table()

    @classmethod
    def modify_style(cls, style: dict[str, Any]):
        style['columns_count'] = 6
        style['header'] = ('#', 'Imie', 'Nazwisko', 'Ranking', '', '')
        style['columns_weights'] = (1, 6, 6, 4, 1, 1)
        style['row_height'] = 25
        style['header_height'] = 35

    def make_action_bar(self):
        return utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.plus_btn,
                         tk.LEFT, tooltip='Stwórz gracza'),
            utils.Action('import.png', self.import_btn,
                         tk.LEFT, tooltip='Importuj graczy'),
            utils.Action('export.png', self.export_btn,
                         tk.LEFT, tooltip='Eksportuj graczy'),
            utils.Action('add.png', self.open_btn,
                         tk.RIGHT, size=(80, 40), tooltip='Dodaj do turnieju'),
        ], (40, 40), bg='#ccc', active_bg='#aaa')

    def update_table(self):
        table_content = []

        for i, player in enumerate(self.players):
            edit_btn = utils.create_image_btn(self.table, 'edit.png', (20, 20),
                                              cmd=lambda idx=i: self.edit_player(idx))
            remove_btn = utils.create_image_btn(self.table, 'minus.png', (20, 20),
                                                cmd=lambda idx=i: self.remove_player(idx))

            table_content.append((i + 1, player.name, player.surname, player.rating, edit_btn, remove_btn))

        self.table.update_table(table_content)
        self.auto_save()

    def edit_player(self, player_idx: int):
        player_copy = copy(self.players[player_idx])

        def on_save():
            if player_copy != self.players[player_idx] and player_copy in self.players:
                raise WindowException(Config.Messages.PLAYER_ALREADY_EXISTS)

            self.players[player_idx] = player_copy
            self.update_table()

        PlayerEditorWindow(self, player_copy, on_save)

    def remove_player(self, player_idx: int):
        def remove():
            del self.players[player_idx]
            self.update_table()

        confirm(self, f'usunąć gracza "{self.players[player_idx]}"', remove)

    def plus_btn(self):
        new_player = Player.create_player(
            name='', surname='', gender=Gender.Men, rating=1000
        )

        def on_save():
            if new_player in self.players:
                raise WindowException(Config.Messages.PLAYER_ALREADY_EXISTS)

            self.players.append(new_player)
            self.update_table()

        PlayerEditorWindow(self, new_player, on_save)

    def import_btn(self):
        if filepath := askopenfilename(filetypes=EXPORT_IMPORT_FILE_EXT, defaultextension='players'):
            try:
                players = MainDB.load_players(path=filepath)
            except UnpicklingError:
                raise AssertionError(WindowException(Config.Messages.PLAYER_IMPORTING_ERROR))

            for player in players:
                if player not in self.players:
                    self.players.append(player)

            self.update_table()
            self.winfo_toplevel().lift()

    def export_btn(self):
        if len(self.table.get_selection()) == 0:
            raise WindowException(Config.Messages.PLAYER_NOT_SELECTED)

        if filepath := asksaveasfilename(filetypes=EXPORT_IMPORT_FILE_EXT, defaultextension='players'):
            selected_players = [self.players[i] for i in self.table.get_selection()]
            MainDB.save_players(selected_players, path=filepath)

    def open_btn(self):
        selected_players = [self.players[idx] for idx in self.table.get_selection()]

        self.add_to_tournament(selected_players)

    def auto_save(self):
        MainDB.save_players(self.players)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    PlayerBrowserWindow(root, lambda x: print('Added:\n', '\n'.join(map(str, x)), sep=''))
    root.mainloop()
