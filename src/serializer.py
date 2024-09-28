from abc import ABC, abstractmethod
from datetime import datetime
from types import NoneType
from typing import Any, Union

from src.tournament import scoring
from src.tournament.interactive_tournament import InteractiveTournament, TournamentData
from src.tournament.player import Player
from src.tournament.round import GameResult
from src.tournament.tournament import TournamentSettings

BASIC_FLAT_TYPES = (str, int, float, bool, NoneType)

type BasicSerializableType = dict | list | Union[*BASIC_FLAT_TYPES]


class Serializer(ABC):
    @abstractmethod
    def can_serialize(self, value: Any) -> bool:
        ...

    def get_unique_id(self) -> str | int:
        return '@' + self.__class__.__name__

    def super_encode(self, obj: Any) -> BasicSerializableType:
        raise NotImplementedError

    def super_decode(self, data: BasicSerializableType) -> Any:
        raise NotImplementedError

    @abstractmethod
    def encode(self, obj: Any) -> BasicSerializableType:
        ...

    @abstractmethod
    def decode(self, data: BasicSerializableType) -> Any:
        ...


class DefaultSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) in BASIC_FLAT_TYPES

    def encode(self, obj: BASIC_FLAT_TYPES) -> BasicSerializableType:
        return obj

    def decode(self, data: BasicSerializableType) -> BASIC_FLAT_TYPES:
        return data


class NestedSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) in (dict, list)

    def encode(self, obj: BASIC_FLAT_TYPES) -> BasicSerializableType:
        if type(obj) is list:
            return [self.super_encode(item) for item in obj]
        else:
            return {key: self.super_encode(value) for key, value in obj.items()}

    def decode(self, data: BasicSerializableType) -> BASIC_FLAT_TYPES:
        if type(data) is list:
            return [self.super_decode(item) for item in data]
        else:
            return {key: self.super_decode(value) for key, value in data.items()}


class InteractiveTournamentSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) is InteractiveTournament

    def encode(self, value: InteractiveTournament) -> BasicSerializableType:
        return self.super_encode({
            'data': value.data,
            'players': list(value.players),
            'rounds': [
                [
                    [list(pair) for pair in value.get_round(i).pairs],
                    value.get_round(i).results,
                ]
                for i in range(value.round_count)
            ],
            'is_finished': value.is_finished(),
            'settings': value.get_settings(),
        })

    def decode(self, data: BasicSerializableType) -> InteractiveTournament:
        data = self.super_decode(data)

        tournament = InteractiveTournament()
        tournament.set_settings(data['settings'])

        for player_data in data['players']:
            player = player_data
            tournament.add_player(player)

        for round_data in data['rounds']:
            pairs, results = round_data

            tournament.next_round(tuple((a, b) for a, b in pairs))

            for table, result in enumerate(results):
                tournament.set_result(table, result)

        if data['is_finished']:
            tmp_func = getattr(tournament, '_update_ratings')
            setattr(tournament, '_update_ratings', lambda *_: 0)
            tournament.finish()
            setattr(tournament, '_update_ratings', tmp_func)

        tournament.data = data['data']

        return tournament


class PlayerSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) is Player

    def encode(self, obj: Player) -> BasicSerializableType:
        return {
            'name': obj.name,
            'rating': obj.rating,
            'hash_id': obj.hash_id,
        }

    def decode(self, data: BasicSerializableType) -> Player:
        return Player(data['name'], rating=data['rating'], hash_id=data['hash_id'])


class GameResultSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) is GameResult

    def encode(self, value: GameResult | None) -> BasicSerializableType:
        return value.name if value is not None else None

    def decode(self, data: BasicSerializableType) -> GameResult | None:
        return GameResult[data]


class TournamentSettingsSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) is TournamentSettings

    def encode(self, value: TournamentSettings) -> BasicSerializableType:
        ok = False
        scorer_name = value.scorer.__class__.__name__

        for scorer in scoring.ALL_SCORERS:
            if scorer.__name__ == scorer_name:
                ok = True

        if not ok:
            raise ValueError(f'Unknown Scorer {scorer_name} (while encoding)')

        return {
            'elo_k_value': value.elo_k_value,
            'scorer': scorer_name,
        }

    def decode(self, data: BasicSerializableType) -> TournamentSettings:
        for scorer in scoring.ALL_SCORERS:
            if scorer.__name__ == data['scorer']:
                return TournamentSettings(elo_k_value=data['elo_k_value'], scorer=scorer())

        raise ValueError(f'Unknown Scorer {data['scorer']} (while decoding)')


class TournamentDataSerializer(Serializer):
    def can_serialize(self, value) -> bool:
        return type(value) is TournamentData

    def encode(self, value: TournamentData) -> BasicSerializableType:
        return {
            'name': value.name,
            'category': value.category,
            'start_timestamp': self._encode_time(value.start_timestamp),
            'finish_timestamp': self._encode_time(value.finish_timestamp),
        }

    @staticmethod
    def _encode_time(time_datetime):
        if time_datetime is None:
            return None

        return time_datetime.timestamp()  # TODO: check if it saves as correct UTC

    def decode(self, data: BasicSerializableType) -> TournamentData:
        return TournamentData(
            name=data['name'],
            category=data['category'],
            start_timestamp=self._decode_time(data['start_timestamp']),
            finish_timestamp=self._decode_time(data['finish_timestamp']),
        )

    @staticmethod
    def _decode_time(time_utc):
        if time_utc is None:
            return None

        return datetime.fromtimestamp(time_utc)
