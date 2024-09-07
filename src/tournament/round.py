from src.serializer import CopyFieldsSerializer


class Round:
    def __init__(self, no_players: int, pairs: tuple[tuple[int, int], ...]):
        self.no_players = no_players
        self.pairs = pairs
        self.pause: set[int] = set()
        self.results: list[tuple[float, float] | None] = [None for _ in pairs]

        self.__test_pairing_and_make_pause()

    def __test_pairing_and_make_pause(self):
        if len(self.pairs) == 0:
            raise ValueError("Pairs cannot be empty")

        players: set[int] = {player_id for pair in self.pairs for player_id in pair}

        if len(players) != len(self.pairs) * 2:
            raise ValueError("One player cannot play twice in one round")

        self.pause = set(range(self.no_players))

        for player in players:
            if player < 0 or player >= self.no_players:
                raise ValueError(f"Player with id {player} does not exist")

            self.pause.discard(player)

    def set_result(self, table: int, result_a: float, result_b: float):
        if table < 0 or table >= len(self.pairs):
            raise IndexError

        self.remove_result(table)
        self.results[table] = (result_a, result_b)

    def remove_result(self, table: int):
        if table < 0 or table >= len(self.pairs):
            raise IndexError

        self.results[table] = None

    def is_completed(self) -> bool:
        return all(result is not None for result in self.results)


class RoundSerializer(CopyFieldsSerializer):
    def __init__(self):
        super().__init__(Round, (
            'no_players',
            'pairs',
            'pause',
            'results',
        ))
