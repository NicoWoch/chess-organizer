import json
from datetime import datetime
import unittest

from src.algorithms.constants import Result
from src.player import Player
from src.serializers import deserializer_hook, serializer_hook


class TestPlayerSerialization(unittest.TestCase):
    def setUp(self):
        self.timestamps: list[datetime] = []

    def save_timestamp(self):
        self.timestamps.append(datetime.now())

    def assert_between_timestamps(self, date: datetime, first_id: int):
        if date < self.timestamps[first_id] or date > self.timestamps[first_id + 1]:
            self.fail(f'Date {date} is not between {self.timestamps[first_id]} and {self.timestamps[first_id + 1]}')

    def test_basic_data(self):
        player = Player.create_player('Jan', 'Kowalski', 1234)
        player.rating = 1200
        creation_date = player.creation_date
        ratings_history = player.get_rating_history()

        data = json.dumps(player, default=serializer_hook)
        self.assertIsInstance(data, str)
        player = json.loads(data, object_hook=deserializer_hook)

        self.assertEqual(player.name, 'Jan')
        self.assertEqual(player.surname, 'Kowalski')
        self.assertEqual(player.rating, 1200)
        self.assertEqual(player.get_rating_history()[0][1], 1234)
        self.assertEqual(player.get_rating_history()[1][1], 1200)
        self.assertEqual(player.get_rating_history(), ratings_history)
        self.assertEqual(player.last_played, None)
        self.assertEqual(player.creation_date, creation_date)

    def test_saving_dates(self):
        self.save_timestamp()
        player = Player.create_player('Jan', 'Kowalski', 1234)
        self.save_timestamp()
        player.rating = 1300
        self.save_timestamp()
        player.rating = 1500
        self.save_timestamp()
        player.trigger_playing()
        self.save_timestamp()

        data = json.dumps(player, default=serializer_hook)
        self.assertIsInstance(data, str)
        player = json.loads(data, object_hook=deserializer_hook)

        self.assert_between_timestamps(player.creation_date, 0)
        self.assert_between_timestamps(player.get_rating_history()[0][0], 0)
        self.assert_between_timestamps(player.get_rating_history()[1][0], 1)
        self.assert_between_timestamps(player.get_rating_history()[2][0], 2)
        self.assert_between_timestamps(player.last_played, 3)


class TestTournamentSerialization(unittest.TestCase):
    def test_all_results(self):
        for value in Result:
            data = json.dumps(value, default=serializer_hook)
            self.assertEqual(json.loads(data, object_hook=deserializer_hook), value)

    def test_sample_tournament_1(self):
        # TODO
        self.fail()


if __name__ == '__main__':
    unittest.main()
