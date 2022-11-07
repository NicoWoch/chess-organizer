import tkinter as tk
from collections.abc import Callable
from copy import copy
from tkinter.filedialog import asksaveasfilename, askopenfilename

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
        utils.center_window(self, (480, 550))
        self.minsize(450, 100)

        self.add_to_tournament = add_to_tournament
        self.players = MainDB.load_players()

        self.table.set_columns(('#', 'Imie', 'Nazwisko', 'Ranking', '', ''), (1, 5, 5, 5, 1, 1))
        self.update_table()

        self.bind('<Control-a>', lambda *_: self.table.select_all())
        self.bind('<Control-d>', lambda *_: self.table.remove_selection())

    def make_action_bar(self):
        return utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.plus_btn, tk.LEFT),
            utils.Action('import.png', self.import_btn, tk.LEFT),
            utils.Action('export.png', self.export_btn, tk.LEFT),
            utils.Action('add.png', self.open_btn, tk.RIGHT, size=(80, 40)),
        ], (40, 40), tooltips=[
            'Stwórz gracza',
            'Importuj graczy',
            'Eksportuj graczy',
            'Dodaj do turnieju',
        ])

    def update_table(self):
        self.table.clear_rows()

        for i, player in enumerate(self.players):
            edit_btn = utils.create_image_btn(None, 'edit.png', (20, 20), cmd=lambda idx=i: self.edit_player(idx))
            remove_btn = utils.create_image_btn(None, 'minus.png', (20, 20), cmd=lambda idx=i: self.remove_player(idx))
            self.table.add_row(i + 1, player.name, player.surname, player.rating, edit_btn, remove_btn)

        self.table.redraw_rows()
        self.auto_save()

    def edit_player(self, player_idx: int):
        player_copy = copy(self.players[player_idx])

        def on_save():
            assert player_copy not in self.players or \
                   player_copy == self.players[player_idx], WindowException(Config.ErrorMsg.PLAYER_ALREADY_EXISTS)

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
            assert new_player not in self.players, WindowException(Config.ErrorMsg.PLAYER_ALREADY_EXISTS)

            self.players.append(new_player)
            self.update_table()

        PlayerEditorWindow(self, new_player, on_save)

    def import_btn(self):
        if filepath := askopenfilename(filetypes=EXPORT_IMPORT_FILE_EXT, defaultextension='players'):
            players = MainDB.load_players(path=filepath)

            for player in players:
                if player not in self.players:
                    self.players.append(player)

            self.update_table()
            self.winfo_toplevel().lift()

    def export_btn(self):
        assert len(self.table.get_selection()) > 0, WindowException(Config.ErrorMsg.PLAYER_NOT_SELECTED)

        if filepath := asksaveasfilename(filetypes=EXPORT_IMPORT_FILE_EXT, defaultextension='players'):
            selected_players = [self.players[i] for i in self.table.get_selection()]
            MainDB.save_players(selected_players, path=filepath)

    def open_btn(self):
        selected_players = [self.players[idx] for idx in self.table.get_selection()]

        assert len(selected_players) > 0, WindowException(Config.ErrorMsg.PLAYER_NOT_SELECTED_FOR_OPEN)

        self.add_to_tournament(selected_players)

    def auto_save(self):
        MainDB.save_players(self.players)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    PlayerBrowserWindow(root, lambda x: print('Added:\n', '\n'.join(map(str, x)), sep=''))
    root.mainloop()
