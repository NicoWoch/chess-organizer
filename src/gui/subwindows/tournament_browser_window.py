import tkinter as tk
from collections.abc import Callable

from src.gui import utils
from src.config import Config
from src.db import MainDB
from src.gui.subwindows.browser_window import BrowserWindow
from src.gui.subwindows.info.confirm_window import confirm
from src.gui.subwindows.info.error_window import WindowException
from src.gui.subwindows.tournament_creation_window import TournamentCreationWindow


class TournamentBrowserWindow(BrowserWindow):
    def __init__(self, parent, open_tournament: Callable, close_tournament: Callable, auto_create=False):
        super().__init__(parent)

        self.title('Wszystkie Turnieje')
        utils.add_icon(self)
        utils.center_window(self, (500, 340))
        self.minsize(500, 100)

        self.open_tournament = open_tournament
        self.close_tournament = close_tournament
        self.tournaments = MainDB.load_tournaments()

        self.table.set_checkmarks_state(False)
        self.table.style['one_select'] = True
        self.table.set_columns(('#', 'Nazwa', 'Gracze', 'Data', ''), (1, 7, 2, 5, 1))
        self.update_table()

        if auto_create:
            self.after(100, lambda: self.plus_btn())

    def make_action_bar(self):
        return utils.create_image_action_bar(self, [
            utils.Action('plus.png', self.plus_btn, tk.LEFT),
            utils.Action('open.png', self.open_btn, tk.RIGHT, size=(80, 40)),
        ], (40, 40), tooltips=[
            'Stwórz turniej',
            'Otwórz turniej',
        ])

    def update_table(self):
        self.table.clear_rows()

        for i, tournament in enumerate(self.tournaments):
            remove_btn = utils.create_image_btn(None, 'minus.png', (20, 20), cmd=lambda idx=i: self.remove_tournament(idx))
            date = tournament.started_date.strftime("%d %B %Y") if tournament.started_date is not None else '-'
            self.table.add_row(i + 1, tournament.name, len(tournament.players), date, remove_btn)

        self.table.redraw_rows()
        self.auto_save()

    def plus_btn(self):
        def on_create(tournament):
            if tournament.name in [t.name for t in self.tournaments]:
                raise WindowException(Config.Messages.TOURNAMENT_ALREADY_EXISTS)

            self.tournaments.insert(0, tournament)
            self.update_table()

            self.open_tournament(tournament)
            self.destroy()

        TournamentCreationWindow(self, on_create)

    def remove_tournament(self, index):
        def remove():
            del self.tournaments[index]
            self.update_table()
            self.close_tournament()

        confirm(self, f'usunąć turniej "{self.tournaments[index].name}"', remove)

    def open_btn(self):
        selected_ids = list(self.table.get_selection())

        if len(selected_ids) == 0:
            raise WindowException(Config.Messages.TOURNAMENT_NOT_SELECTED_FOR_OPEN)

        self.open_tournament(self.tournaments[selected_ids[0]])
        self.destroy()

    def auto_save(self):
        MainDB.save_tournaments(self.tournaments)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    TournamentBrowserWindow(root, lambda x: print('Opening tournament:', x.name), lambda: 0)
    root.mainloop()
