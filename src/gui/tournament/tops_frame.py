import tkinter as tk
from typing import Any

import src.gui.gui_utils as utils
from src.algorithms.game import Result, Game
from src.algorithms.tops import Tops
from src.player import Gender, Player

GAME_SIZE = 15, 30

ONE_COLUMNS = 30,
TWO_COLUMNS = 10, 50
ONE_CONS = ONE_COLUMNS[0] + GAME_SIZE[1] // 2,
TWO_CONS = TWO_COLUMNS[0] + GAME_SIZE[1] // 2, TWO_COLUMNS[1] + GAME_SIZE[1] // 2


class TopsFrame(utils.ResizingCanvas):
    def __init__(self, parent, tops):
        super().__init__(parent, width=100, height=100)

        self.tops = tops
        self.game_stats: list[tuple[Any, int, int]] = []
        self.selected_game: tuple[int, int] = (-1, -1)

        self.make_tops()

        self.bind("<Button-1>", self._set_selection)
        self.bind("<Button-3>", self._remove_selection)

    def make_tops(self):
        if len(self.tops.rounds) == 1:
            self.make_board_row(0, 0, 50, ONE_COLUMNS, outline='gold')
        elif len(self.tops.rounds) == 2:
            self.make_board_row(0, 0, 33, TWO_COLUMNS, outline='green')
            self.create_connections(33, 66, TWO_CONS, ONE_CONS)
            self.make_board_row(1, 0, 66, ONE_COLUMNS, outline='gold')
        elif len(self.tops.rounds) == 3:
            self.make_board_row(0, 0, 11, TWO_COLUMNS)
            self.create_connections(11, 31, TWO_CONS, ONE_CONS, arrow_size=2)
            self.make_board_row(1, 0, 31, ONE_COLUMNS, outline='green')
            self.create_connections(31, 50, ONE_CONS, ONE_CONS, arrow_size=2)
            self.make_board_row(2, 0, 50, ONE_COLUMNS, outline='gold')
            self.create_connections(50, 69, ONE_CONS, ONE_CONS, is_arrow_left=True, arrow_size=2)
            self.make_board_row(1, 1, 69, ONE_COLUMNS, outline='green')
            self.create_connections(69, 90, ONE_CONS, TWO_CONS, is_arrow_left=True, arrow_size=2)
            self.make_board_row(0, 2, 90, TWO_COLUMNS)
        else:
            raise Exception(f'Cannot display {len(self.tops.rounds)} number of rounds in tops')

    def redraw(self):
        self.delete('all')
        self.game_stats.clear()

        scale_x, scale_y = self.width / 100, self.height / 100
        print(scale_x, scale_y)

        self.make_tops()
        self.scale('all', 0, 0, scale_x, scale_y)

    def create_connections(self, x_in, x_out, y_ins, y_outs, is_arrow_left=False, arrow_size=4):
        x_in += GAME_SIZE[0] // 2 + 1
        x_out -= GAME_SIZE[0] // 2
        arrowshape = (8 * arrow_size, 10 * arrow_size, 3 * arrow_size)
        for y_in in y_ins:
            for y_out in y_outs:
                half_x = (x_in + x_out) // 2
                self.create_line(x_in, y_in, half_x, y_in, width=3, arrow='first' if is_arrow_left else None, arrowshape=arrowshape)
                self.create_line(half_x, y_in, half_x, y_out, width=3)
                self.create_line(half_x, y_out, x_out, y_out, width=3, arrow='last' if not is_arrow_left else None, arrowshape=arrowshape)

    def make_board_row(self, round_id: int, start_table_id: int, x: int, columns: tuple[int, ...], outline='blue'):
        x -= GAME_SIZE[0] // 2
        for i, col in enumerate(columns):
            table_id = start_table_id + i

            if self.selected_game == (round_id, table_id):
                game_obj = self.create_game(x, col, self.tops.rounds[round_id][table_id], 'red', 5)
            else:
                game_obj = self.create_game(x, col, self.tops.rounds[round_id][table_id], outline, 2)

            self.game_stats.append((game_obj, round_id, table_id))

    def create_game(self, x, y, game: Game, outline, outlinewidth):
        rect = utils.Rect(x, y, x + GAME_SIZE[0], y + GAME_SIZE[1])
        game_obj = self.create_game_bg(rect, outline, outlinewidth)
        self.create_game_texts(rect, game)
        self.create_game_result(rect, game.result)
        return game_obj

    def create_game_bg(self, rect: utils.Rect, outline: str, outlinewidth: int):
        game_obj = self.create_rectangle(*rect.nw, *rect.se)
        self.create_rectangle(rect.w, rect.n, rect.e, rect.center[1], fill='white', outline=outline, width=outlinewidth)
        self.create_rectangle(rect.w, rect.center[1], rect.e, rect.s, fill='black', outline=outline, width=outlinewidth)
        return game_obj

    def create_game_texts(self, rect: utils.Rect, game: Game):
        font = ('Calibri', 15)
        if game.white is not None:
            self.create_text(rect.center[0], rect.n + (rect.height // 4) - 2, text=game.white.name, font=font)
            self.create_text(rect.center[0], rect.n + (rect.height // 4) + 2, text=game.white.surname, font=font)

        if game.black is not None:
            self.create_text(rect.center[0], rect.s - (rect.height // 4) - 2, text=game.black.name, fill='white', font=font)
            self.create_text(rect.center[0], rect.s - (rect.height // 4) + 2, text=game.black.surname, fill='white', font=font)

    def create_game_result(self, rect: utils.Rect, result: Result):
        if result == Result.White:
            self.create_x(utils.Rect(rect.w, rect.center[1], *rect.se), fill='red', width=3)
        elif result == Result.Black:
            self.create_x(utils.Rect(*rect.nw, rect.e, rect.center[1]), fill='red', width=3)
        elif result == Result.Draw:
            raise Exception('Cannot draw in tops')
        else:
            pass

    def create_x(self, rect, **kwargs):
        self.create_line(*rect.nw, *rect.se, **kwargs)
        self.create_line(*rect.ne, *rect.sw, **kwargs)

    def _set_selection(self, event):
        for game_stat in self.game_stats:
            coords = self.coords(game_stat[0])
            if coords[0] <= event.x <= coords[2] and \
               coords[1] <= event.y <= coords[3]:
                self.selected_game = game_stat[1:]
                self.redraw()
                break

    def _remove_selection(self, _):
        self.selected_game = (-1, -1)
        self.redraw()

    def set_result(self, result: Result):
        pass


if __name__ == '__main__':  # Testing tops frame
    root = tk.Tk()
    root.geometry('1000x600')
    TopsFrame(root, Tops([
        Player.create_player(name='Łukasz',     surname='Nowak', gender=Gender.Men, rating=1200),
        Player.create_player(name='Adam',       surname='Nowak', gender=Gender.Women, rating=1100),
        Player.create_player(name='Anna',       surname='Nowak', gender=Gender.Other, rating=3000),
        Player.create_player(name='Eugene',     surname='Kowalski', gender=Gender.Men, rating=800),
        Player.create_player(name='Władysław',  surname='Kowalski', gender=Gender.Other, rating=3200),
        Player.create_player(name='Wołomir',    surname='Kowalski', gender=Gender.Men, rating=990),
        Player.create_player(name='Nicolas',    surname='Kowalski', gender=Gender.Men, rating=1200),
        Player.create_player(name='Jarek',      surname='Kowalski', gender=Gender.Women, rating=1100),
    ], [
        8, 7, 6, 5, 4, 3, 2, 1
    ])).pack(fill='both', expand=True, padx=100, pady=50)
    root.mainloop()

