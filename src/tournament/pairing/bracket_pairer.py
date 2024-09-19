from abc import ABC, abstractmethod

from src.tournament.pairing.pairer import Pairer, ListPairs
from src.tournament.round import Pairs
import logging

logger = logging.getLogger(__name__)

type Bracket = tuple[float, set[int]]


class BracketPairer(Pairer, ABC):
    def _pair(self) -> Pairs:
        if self.stats.round_count == 0:
            return self._pair_first_round()

        return self.__pair_middle_round()

    @abstractmethod
    def _pair_first_round(self) -> Pairs:
        ...

    def __pair_middle_round(self) -> Pairs:
        brackets = self.__create_pairing_brackets()

        return tuple(self.__pair_brackets(brackets))

    def __create_pairing_brackets(self) -> list[Bracket]:
        brackets: list[Bracket] = [(-1, set())]

        for player in sorted(self.players, key=lambda p: -self.scores[p][0]):
            if self.scores[player][0] == brackets[-1][0]:
                brackets[-1][1].add(player)
            else:
                brackets.append((self.scores[player][0], {player}))

        return brackets[1:]

    def __pair_brackets(self, brackets: list[Bracket]) -> ListPairs:
        logger.info(f'Pairing {len(self.players)} players')
        logger.info(f'Brackets: {brackets}')
        logger.debug('Pairing without breaking...')

        paired_brackets_by_level: list[tuple[ListPairs, set[int]]] = [([], set())]
        paired_brackets_by_level += self.__pair_brackets_without_breaking([players for _, players in brackets])

        logger.debug(f'First Paired Brackets: {[level[0] for level in paired_brackets_by_level[1:]]}')
        logger.debug(f'First Downfloats: {paired_brackets_by_level[-1][1]}')

        while len(paired_brackets_by_level[-1][1]) > 1:
            logger.debug('Breaking last bracket!')

            if len(paired_brackets_by_level) <= 2:
                raise Exception('Cannot pair players')

            pairs_2, downfloat_2 = paired_brackets_by_level.pop()
            pairs_1, downfloat_1 = paired_brackets_by_level.pop()

            players = self.__break_pairs(pairs_1) | self.__break_pairs(pairs_2) | downfloat_2
            downfloat = paired_brackets_by_level[-1][1]

            pairs = self._pair_bracket(players.copy(), downfloat.copy(), is_last=True)
            next_downfloat = self.__get_unpaired(players, downfloat, pairs)

            paired_brackets_by_level.append((pairs, next_downfloat))

            logger.debug(f'\tNew Downfloats: {paired_brackets_by_level[-1][1]}')

        pairs = [pair for pairs, _ in paired_brackets_by_level for pair in pairs]

        logger.info(f'Paired: {pairs}')
        return pairs

    @staticmethod
    def __break_pairs(pairs: ListPairs) -> set[int]:
        return {player for pair in pairs for player in pair}

    def __pair_brackets_without_breaking(self, brackets: list[set[int]]) -> list[tuple[ListPairs, set[int]]]:
        paired_brackets_by_levels: list[tuple[ListPairs, set[int]]] = []
        downfloat: set[int] = set()

        for i, players in enumerate(brackets):
            is_last = i == len(brackets) - 1

            pairs = self._pair_bracket(players.copy(), downfloat.copy(), is_last=is_last)
            downfloat = self.__get_unpaired(players, downfloat, pairs)

            paired_brackets_by_levels.append((pairs, downfloat.copy()))

        return paired_brackets_by_levels

    @staticmethod
    def __get_unpaired(players: set[int], downfloat: set[int], pairs: ListPairs) -> set[int]:
        unpaired = players | downfloat
        unpaired.difference_update({player for pair in pairs for player in pair})
        return unpaired

    @abstractmethod
    def _pair_bracket(self, players: set[int], downfloat: set[int], *, is_last: bool) -> ListPairs:
        ...
