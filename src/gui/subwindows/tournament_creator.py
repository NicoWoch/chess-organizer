import tkinter as tk
from tkinter import ttk
from typing import Callable

from src.gui.validation_utils import tk_validator, tk_unsigned_float_validator
from src.gui.widgets.transient_toplevel import TransientToplevel
from src.tournament import scoring
from src.tournament.interactive_tournament import InteractiveTournament, TournamentData
from src.tournament.scoring import BuchholzScorer
from src.tournament.scoring.scorer import Scorer
from src.tournament.tournament import TournamentSettings


class TournamentCreator(TransientToplevel):
    def __init__(self, parent, on_create: Callable[[InteractiveTournament], None]):
        super().__init__(parent)

        self._parent_on_create = on_create

        self.name = tk.StringVar(self, value='')
        self.elo_k_value = tk.DoubleVar(self, value=40)
        self.scorer = tk.StringVar(self, value=self._scorer_to_string(BuchholzScorer))

        self.__define_layout()

    def __define_layout(self):
        self.title("Nowy Turniej")
        self.maxsize(600, 600)
        self.minsize(280, 350)
        ttk.Style().theme_use('clam')

        title_label = ttk.Label(self, text='Utwórz Turniej', font=('Comic Sans MS', 22))
        adv_section = ttk.Labelframe(self, text='Zaawansowane:')

        name_label = ttk.Label(self, text='Nazwa turnieju:')
        name_entry = ttk.Entry(self, textvariable=self.name)

        elo_label = ttk.Label(adv_section, text='Elo K:')
        elo_entry = ttk.Entry(adv_section, textvariable=self.elo_k_value, **tk_unsigned_float_validator(self))

        scorer_label = ttk.Label(adv_section, text='Punkty:')
        scorer_entry = ttk.Combobox(adv_section, textvariable=self.scorer,
                                    values=list(map(self._scorer_to_string, scoring.ALL_SCORERS)),
                                    **self._scorer_validator())

        create_btn = ttk.Button(self, text='Stwórz', command=self._on_create)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        title_label.grid(row=0, column=0, columnspan=2, pady=30)
        name_label.grid(row=1, column=0)
        name_entry.grid(row=1, column=1)
        create_btn.grid(row=2, column=0, columnspan=2, pady=20)
        adv_section.grid(row=3, column=0, columnspan=2, padx=30, pady=(0, 30), ipadx=30, ipady=30)

        adv_section.rowconfigure(0, weight=1)
        adv_section.rowconfigure(1, weight=1)
        adv_section.columnconfigure(0, weight=1)
        adv_section.columnconfigure(1, weight=1)

        elo_label.grid(row=0, column=0)
        elo_entry.grid(row=0, column=1)
        scorer_label.grid(row=1, column=0)
        scorer_entry.grid(row=1, column=1)

    @tk_validator
    def _scorer_validator(self, text: str):
        return len(self._find_scorers(text)) != 0

    @staticmethod
    def _scorer_to_string(scorer: type[Scorer]) -> str:
        return scorer.__name__

    @staticmethod
    def _find_scorers(string: str) -> list[type[Scorer]]:
        return [scorer for scorer in scoring.ALL_SCORERS if scorer.__name__ == string]

    def _on_create(self):
        self.destroy()

        it = InteractiveTournament(TournamentData(
            name=self.name.get(),
            category='',
        ))

        it.set_settings(TournamentSettings(
            elo_k_value=self.elo_k_value.get(),
            scorer=self._find_scorers(self.scorer.get())[0](),
        ))

        self._parent_on_create(it)
