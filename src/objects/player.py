from dataclasses import dataclass


@dataclass
class Player:
    name = ''
    surname = ''
    rating = 0
    tournament_stats = {}
