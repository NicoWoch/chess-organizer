import tkinter as tk
from typing import Callable

from src.gui.widgets.transient_toplevel import TransientToplevel
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.round_stats import RoundStats


class TournamentDataView(TransientToplevel):
    def __init__(self, parent, get_tournament: Callable[[], InteractiveTournament | None]):
        super().__init__(parent)

        self._get_tournament = get_tournament
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.update_btn = tk.Button(self, text='Aktualizuj', command=self.update_data)
        self.update_btn.place(relx=1, x=-105, y=5, width=100, height=50)

        self.title('Dane Turnieju')
        self.geometry('600x400')
        self.update_data()

    def __clear_widget(self, widget=None):
        if widget is None:
            widget = self.container

        for child in widget.winfo_children():
            self.__clear_widget(child)

        if widget != self.container:
            widget.destroy()

    def update_data(self):
        self.show_tournament_data(self._get_tournament())

    def show_tournament_data(self, tournament: InteractiveTournament | None):
        self.__clear_widget()

        if tournament is None:
            label = tk.Label(self.container, text='Brak Otwartego Turnieju', font=('Comic Sans MS', 20))
            label.pack(side=tk.TOP)
            return

        text = tk.Text(self.container)
        text.pack(fill=tk.BOTH, expand=True)

        self.__show_tournament_info(text, tournament)

        for i in range(tournament.round_count):
            self.__show_stats(text, i, tournament.get_stats(i))

    @staticmethod
    def __show_tournament_info(text, tournament: InteractiveTournament):
        text.insert(tk.END, f'Turniej "{tournament.data.name}" w kategorii "{tournament.data.category}"\n')
        text.insert(tk.END, f'Gracze:\n')

        for player in tournament.players:
            text.insert(tk.END, f'\t- {player}\n')

    @staticmethod
    def __show_stats(text, round_no: int, stats: RoundStats):
        text.insert(tk.END, f' Runda {round_no} '.center(20, '-') + '\n')
        text.insert(tk.END, f'Rankingi: {stats.ratings}\n')
        text.insert(tk.END, f'Balans Kolorów: {stats.color_balance}\n')
        text.insert(tk.END, f'Pauzy: {stats.paused}\n')
        text.insert(tk.END, f'Powtórzenia Kolorów: {stats.color_repetition}\n')
        text.insert(tk.END, '--- ' * 5 + '\n')
        text.insert(tk.END, f'Wygrane: {stats.wins}\n')
        text.insert(tk.END, f'Remisy: {stats.draws}\n')
        text.insert(tk.END, f'Przegrane: {stats.losses}\n')
