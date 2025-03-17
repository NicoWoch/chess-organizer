import logging
from abc import ABC, abstractmethod
from typing import Any

from src.algorithms.tournament import Pairer, Tournament, Pairs

type PairsSet = set[tuple[int, int]]


class BracketPairer(Pairer, ABC):
    tournament: Tournament

    def pair_next_round(self) -> Pairs:
        logging.debug(f'Pairing {len(self.tournament.rounds) + 1}. round of tournament'
                      f'\"{self.tournament.name}\" with {self.tournament.players_count} players')

        if len(self.tournament.rounds) == 0:
            return self.__pair_first_round()

        self._prepare_for_pairing()
        return self.__pair_with_brackets()

    @abstractmethod
    def __pair_first_round(self) -> Pairs: ...

    def _prepare_for_pairing(self):
        self.points = self.tournament.calculate_points()
        self.has_paused = {
            pause
            for i in range(len(self.tournament.rounds))
            for pause in self.tournament.calculate_pause_indices(i)
        }

    def __pair_with_brackets(self) -> Pairs:
        player_groups = self.__create_player_groups()
        brackets: list[PairsSet] = []
        downfloat = set()

        for _, group in player_groups:
            pairs, downfloat = self.__pair_bracket_with_downfloat(group | downfloat)
            brackets.append(pairs)

        while len(brackets) != 0 and not self.__is_correct_pause(downfloat):
            self.__break_last_bracket(brackets, downfloat)

        logging.debug(f'Paired using brackets: {len(player_groups)} brackets -> {len(brackets)} brackets')

        final_pairs = (pair for bracket in brackets for pair in bracket)
        return tuple(sorted(final_pairs, key=self._pairs_order_key))

    def __create_player_groups(self) -> list[tuple[float, set[int]]]:
        players_groups = [
            (big, {i for i, p in enumerate(self.points) if p.big == big})
            for big in set(p.big for p in self.points)
        ]

        players_groups.sort(key=lambda x: x[0], reverse=True)

        return players_groups

    def __is_correct_pause(self, downfloat: set[int]) -> bool:
        if len(downfloat) == 0:
            return True

        return len(downfloat) == 1 and list(downfloat)[0] not in self.has_paused

    def __break_last_bracket(self, brackets: list[PairsSet], downfloat: set[int]):
        bracket_1 = {player for pair in brackets.pop() for player in pair}
        bracket_2 = {player for pair in brackets.pop() for player in pair}

        pairs, new_downfloat = self.__pair_bracket_with_downfloat(bracket_1 | bracket_2 | downfloat)
        brackets.append(pairs)
        downfloat.clear()
        downfloat.union(new_downfloat)

    def __pair_bracket_with_downfloat(self, bracket: set[int]) -> tuple[PairsSet, set[int]]:
        pairs = self._pair_bracket(bracket)
        return pairs, bracket.copy() - {player for pair in pairs for player in pair}

    @abstractmethod
    def _pair_bracket(self, bracket: set[int]) -> PairsSet: ...

    @abstractmethod
    def _pairs_order_key(self, pair: tuple[int, int]) -> Any: ...
