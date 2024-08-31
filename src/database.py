import json
import os
from abc import ABC, abstractmethod
import dataclasses
from typing import Any


class DatabaseSerializer(ABC):
    @abstractmethod
    def serialize(self, data: Any) -> dict | Any: ...

    @abstractmethod
    def deserialize(self, data: dict | Any) -> Any: ...


class DefaultDatabaseSerializer(DatabaseSerializer):
    def serialize(self, data: Any) -> dict | Any:
        if isinstance(data, dict) or isinstance(data, list):
            return data

        return json.JSONEncoder().default(data)

    def deserialize(self, data: dict | Any) -> Any:
        return data


class SerializerUnion(DatabaseSerializer):
    def __init__(self, *serializers: DatabaseSerializer):
        self._serializers = serializers

    def serialize(self, data: Any) -> dict | Any:
        for serializer in self._serializers:
            data = serializer.serialize(data)

        return data

    def deserialize(self, data: dict) -> Any:
        for serializer in reversed(self._serializers):
            data = serializer.deserialize(data)

        return data


class Database:
    def __init__(self, filename: str, *serializers: DatabaseSerializer):
        self._filename = filename if filename.endswith('.json') else (filename + '.json')
        self._serializer = SerializerUnion(*serializers, DefaultDatabaseSerializer())

    def write(self, data: Any):
        with open(self._filename, 'w') as f:
            json.dump(data, f, default=self._serializer.serialize)

    def read(self) -> Any:
        if not os.path.isfile(self._filename):
            self.write(None)

        with open(self._filename, 'r') as f:
            return json.load(f, object_hook=self._serializer.deserialize)
