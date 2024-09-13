from enum import Enum

type Pairs = tuple[tuple[int, int], ...]


class GameResult(Enum):
    WIN = (1, 0), True
    DRAW = (.5, .5), True
    LOSE = (0, 1), True
    PLAYER_A_NOT_SHOWED_IN_TIME = (0, 1), False
    PLAYER_B_NOT_SHOWED_IN_TIME = (1, 0), False
    BOTH_PLAYERS_NOT_SHOWED_IN_TIME = (0, 0), False

    @property
    def points_a(self):
        return self.value[0][0]

    @property
    def points_b(self):
        return self.value[0][1]

    @property
    def is_rated(self):
        return self.value[1]


class Round:
    def __init__(self, no_players: int, pairs: Pairs):
        self.no_players = no_players
        self.pairs = pairs
        self.pause: set[int] = set()
        self.results: list[GameResult | None] = [None for _ in pairs]

        self.__test_pairing_and_make_pause()

    def __test_pairing_and_make_pause(self):
        players: set[int] = {player_id for pair in self.pairs for player_id in pair}

        if len(players) != len(self.pairs) * 2:
            raise ValueError("One player cannot play twice in one round")

        self.pause = set(range(self.no_players))

        for player in players:
            if player < 0 or player >= self.no_players:
                raise ValueError(f"Player with id {player} does not exist")

            self.pause.discard(player)

    def set_result(self, table: int, result: GameResult | None):
        if table < 0 or table >= len(self.pairs):
            raise IndexError

        self.results[table] = result

    def is_completed(self) -> bool:
        return all(result is not None for result in self.results)
