import os
import webbrowser
from tkinter.filedialog import asksaveasfile

from fpdf import FPDF

from src.algorithms.constants import Game, Result, Points
from src.config import Config
from src.pdf.table_generator import PdfTableGenerator
from src.player import Player


def make_starting_list_pdf(tournament_name: str, players: list[Player]) -> FPDF:
    table = [['#', 'Gracz', 'Ranking']]

    for i, player in enumerate(players):
        table.append([
            i + 1,
            player,
            player.rating,
        ])

    return PdfTableGenerator(
        tournament_name, 'Lista Startowa',
        table, column_weights=[1, 3, 2]
    ).generate_fpdf()


def make_pairings_pdf(tournament_name: str, round_id: int, pairs: list[Game], pause_players: list[Player]) -> FPDF:
    table = [['#', 'Białe', 'Czarne', 'Wynik']]

    for i, game in enumerate(pairs):
        table.append([
            i + 1,
            game.white,
            game.black,
            game.result.value,
        ])

    for player in pause_players:
        table.append([
            len(table),
            player,
            '** PAUZA **',
            Result.White.value
        ])

    return PdfTableGenerator(
        tournament_name, f'Runda {round_id + 1}',
        table, column_weights=[1, 4, 4, 2]
    ).generate_fpdf()


def make_results_pdf(tournament_name: str, scoreboard: list[tuple[Player, Points]]) -> FPDF:
    table = [['#', 'Gracz', 'Wynik']]

    position = 0
    last_score = None
    for player, score in scoreboard:
        if last_score != score:
            position += 1

        last_score = score

        table.append([
            position,
            player,
            str(score),
        ])

    return PdfTableGenerator(
        tournament_name, 'Wyniki',
        table, column_weights=[1, 3, 2]
    ).generate_fpdf()




def show_pdf_in_browser(pdf: FPDF, title='temp'):
    tmp_path = os.path.join(Config.TEMP_DIR, title + '.pdf')
    pdf.output(tmp_path)
    webbrowser.open(tmp_path)


def save_pdf_with_dialog(pdf: FPDF):
    filetypes = [('Wszystkie Pliki', '*.*'), ('Pliki PDF', '*.pdf')]
    file = asksaveasfile(title='Wybierz gdzie zapisać pdf', filetypes=filetypes, defaultextension='pdf')

    if file is None:
        return

    file.close()
    pdf.output(file.name)
