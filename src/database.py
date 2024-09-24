import json
import os

from typing import Any

from src import serializer as srl


SERIALIZERS = [
    srl.DefaultSerializer(),
    srl.NestedSerializer(),
    srl.InteractiveTournamentSerializer(),
    srl.PlayerSerializer(),
    srl.GameResultSerializer(),
    srl.TournamentSettingsSerializer(),
]


class Database:
    def __init__(self, filename: str, default_data: Any = None, *serializers: srl.Serializer):
        self._filename = filename if filename.endswith('.json') else (filename + '.json')
        self.default_data = default_data
        self.serializers = SERIALIZERS + list(serializers)

    def _setup_serializers_super_encoders(self):
        for serializer in self.serializers:
            serializer.super_encode = self._encode
            serializer.super_decode = self._decode

    def _encode(self, obj: Any) -> srl.BasicSerializableType:
        for serializer in self.serializers:
            if serializer.can_serialize(obj):
                return {
                    '__serializer__': serializer.get_unique_id(),
                    '__data__': serializer.encode(obj)
                }

        raise ValueError(f'No serializer found for type {type(obj)}')

    def _decode(self, data: srl.BasicSerializableType) -> Any:
        for serializer in self.serializers:
            if data['__serializer__'] == serializer.get_unique_id():
                return serializer.decode(data['__data__'])

        raise ValueError(f'Cannot parse type {type(data)}')

    def write(self, data: Any):
        self._setup_serializers_super_encoders()

        with open(self._filename, 'w') as f:
            json.dump(self._encode(data), f, indent=2)

    def read(self) -> Any:
        self._setup_serializers_super_encoders()

        if not os.path.isfile(self._filename):
            self.write(self.default_data)

        with open(self._filename, 'r') as f:
            return self._decode(json.load(f))
