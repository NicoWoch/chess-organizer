import os
import subprocess
import tempfile
from typing import Optional

from src.algorithms.game import Game, Result
from src.player import Gender, Player

PAIRING_TEMPLATE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        body {{
            text-align: center;
        }}
        table {{
            margin: auto;
            border-collapse: collapse;
        }}
        table, th, td, tr {{
            border: 1px solid;
        }}
        th, td {{
            padding: 10px;
        }}
    </style>
</head>
<body>
    <h2>{tournament_name}</h2>
    <h4>{round_label}</h4>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Białe</th>
                <th>Czarne</th>
                <th>Wynik</th>
            </tr>
        </thead>
        <tbody>
            
            {game_rows}
        </tbody>
    </table>
    {pause_player_html}
    <!-- Made By Chess Organizer -->
</body>
</html>
'''

ROW_TEMPLATE_HTML = '''
<tr>
    <td>{table_no}</td>
    <td>{white}</td>
    <td>{black}</td>
    <td>{result}</td>
</tr>
'''


class PairingPrinter:
    def __init__(self, tournament_name: str, round_no: int, games: list[Game], pause: Optional[Player]):
        self.tournament_name = tournament_name
        self.round_no = round_no
        self.games = games
        self.pause = pause

    def generate_html(self):
        return PAIRING_TEMPLATE_HTML \
            .format(
                tournament_name=self.tournament_name,
                round_label=f'Runda {self.round_no}',
                game_rows=''.join(self._generate_html_game_row(i) for i in range(len(self.games))),
                pause_player_html=f'<h5>Pauza: {self.pause}</h5>' if self.pause is not None else ''
            )

    def _generate_html_game_row(self, game_idx):
        return ROW_TEMPLATE_HTML \
            .format(
                table_no=game_idx + 1,
                white=str(self.games[game_idx].white),
                black=str(self.games[game_idx].black),
                result=self.games[game_idx].result.value
            )

    def save_html_page(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(self.generate_html())

    def show_html_page(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
            tmp.write(self.generate_html())

        os.startfile(tmp.name)


def test():
    print('Start')
    games = [
        Game(
            Player.create_player(name='Jan1', surname='Kom', gender=Gender.Men, rating=1000),
            Player.create_player(name='Jan2', surname='Kom', gender=Gender.Men, rating=1200),
            Result.Playing
        ),
        Game(
            Player.create_player(name='Jan3', surname='Kom', gender=Gender.Men, rating=1300),
            Player.create_player(name='Jan4', surname='Kom', gender=Gender.Men, rating=1400),
            Result.Draw
        ),
        Game(
            Player.create_player(name='Jan5', surname='Kom', gender=Gender.Men, rating=1500),
            Player.create_player(name='Jan6', surname='Kom', gender=Gender.Men, rating=1115),
            Result.Black
        )
    ]

    PairingPrinter('Super Turniej', 1, games, None).show_html_page()


if __name__ == '__main__':
    test()
