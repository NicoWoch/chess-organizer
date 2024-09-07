import json
import os

from typing import Any

from src.serializer import Serializer, BasicSerializableType, BASIC_FLAT_TYPES, DEFAULT_SERIALIZERS


class Database:
    def __init__(self, filename: str, *serializers: Serializer):
        self._filename = filename if filename.endswith('.json') else (filename + '.json')
        self.serializers = DEFAULT_SERIALIZERS + list(serializers)

    def _encode(self, obj: Any) -> BasicSerializableType:
        if type(obj) == list:
            return [self._encode(item) for item in obj]
        elif type(obj) == dict and all(type(key) in BASIC_FLAT_TYPES for key in obj):
            return {key: self._encode(value) for key, value in obj.items()}
        elif type(obj) in BASIC_FLAT_TYPES:
            return obj

        good_serializers = [srl for srl in self.serializers if type(obj) == srl.can_serialize()]

        if len(good_serializers) == 0:
            raise ValueError(f'No serializer found for {obj}')
        elif len(good_serializers) > 1:
            raise ValueError(f'Multiple serializers found for {obj}')

        serializer = good_serializers[0]
        serializer_id = serializer.get_unique_id()

        return {
            '__serializer__': serializer_id,
            '__object__': self._encode(serializer.encode(obj)),
        }

    def _decode(self, data: BasicSerializableType) -> Any:
        if isinstance(data, dict) and '__serializer__' in data and '__object__' in data:
            serializer_id = data['__serializer__']
            good_serializers = [srl for srl in self.serializers if srl.get_unique_id() == serializer_id]

            if len(good_serializers) == 0:
                raise ValueError(f'No serializer found with id: {serializer_id}')
            elif len(good_serializers) > 1:
                raise ValueError(f'Multiple serializers found with id: {serializer_id}')

            serializer = good_serializers[0]
            return serializer.decode(data['__object__'], self._decode)

        if isinstance(data, list):
            return [self._decode(item) for item in data]
        elif isinstance(data, dict):
            return {key: self._decode(value) for key, value in data.items()}
        elif isinstance(data, str | int | float | bool | None):
            return data

        raise ValueError(f'Cannot parse type {type(data)}')

    def write(self, data: Any):
        with open(self._filename, 'w') as f:
            json.dump(self._encode(data), f, indent=2)

    def read(self) -> Any:
        if not os.path.isfile(self._filename):
            self.write(None)

        with open(self._filename, 'r') as f:
            return self._decode(json.load(f))
