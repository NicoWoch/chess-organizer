import json
from typing import List


class Player:
    def __init__(self, name, surname, rating, old_ratings):
        self.name = name
        self.surname = surname
        self.rating = rating
        self.old_ratings = old_ratings
        self.tournament_stats = {}

    def get_data(self):
        return [self.name, self.surname, self.rating, self.old_ratings]

    def __eq__(self, other):
        return all(getattr(self, prop) == getattr(other, prop) for prop in ['name', 'surname', 'rating', 'old_ratings'])

    def __str__(self):
        return f"Player('{self.name}', '{self.surname}', {self.rating}, {self.old_ratings})"


def save_players(players: List[Player], file_path):
    json_data = json.dumps([player.get_data() for player in players])

    with open(file_path, 'w') as file:
        file.write(json_data)


def load_players(file_path):
    with open(file_path) as file:
        data = json.loads(file.read())

        for player_data in data:
            yield Player(*player_data)
