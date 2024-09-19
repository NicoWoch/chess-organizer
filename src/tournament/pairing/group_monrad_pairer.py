import itertools

from src.tournament.pairing.pairer import ListPairs, Pairs

from src.tournament.pairing.bracket_pairer import BracketPairer


# TODO: finish and test it


class GroupMonradPairer(BracketPairer):
    def _pair_first_round(self) -> Pairs:
        return tuple((self.players[i], self.players[i + 1]) for i in range(0, len(self.players) - 1, 2))

    def _pair_bracket(self, players: set[int], downfloat: set[int], *, is_last: bool) -> ListPairs:
        players_list = list(players | downfloat)
        best_pairs = []

        for players_perm in itertools.permutations(players_list):
            pairs = [(players_perm[i], players_perm[i + 1]) for i in range(0, len(players_perm) - 1, 2)]
            pairs = list(filter(lambda pair: self.stats.played_together[pair[0]][pair[1]] == 0, pairs))

            if len(pairs) > len(best_pairs):
                best_pairs = pairs

            if len(best_pairs) >= len(players_list) // 2:
                break

        return best_pairs
