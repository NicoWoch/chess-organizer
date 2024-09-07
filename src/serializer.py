from abc import ABC, abstractmethod
from collections import defaultdict
from types import NoneType
from typing import Any, Callable, Union

BASIC_FLAT_TYPES = (str, int, float, bool, NoneType)

type BasicSerializableType = dict | list | Union[*BASIC_FLAT_TYPES]
type DefaultDecoder = Callable[[BasicSerializableType], Any]


class Serializer(ABC):
    @abstractmethod
    def can_serialize(self) -> type | tuple[type, ...]:
        ...

    def get_unique_id(self) -> str | int:
        if isinstance(self.can_serialize(), type):
            return '@' + self.can_serialize().__name__
        else:
            return '@' + '-'.join(cls.__name__ for cls in self.can_serialize())

    @abstractmethod
    def encode(self, obj: Any) -> BasicSerializableType:
        ...

    @abstractmethod
    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        ...


class TupleSerializer(Serializer):
    def can_serialize(self) -> type | tuple[type, ...]:
        return tuple

    def encode(self, obj: Any) -> BasicSerializableType:
        return list(obj)

    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        return tuple(map(default, data))


class SetSerializer(Serializer):
    def can_serialize(self) -> type | tuple[type, ...]:
        return set

    def encode(self, obj: Any) -> BasicSerializableType:
        return list(obj)

    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        return set(map(default, data))


class DefaultDictSerializer(Serializer):
    def can_serialize(self) -> type | tuple[type, ...]:
        return defaultdict

    def encode(self, obj: Any) -> BasicSerializableType:
        if obj.default_factory is int:
            return {'factory': 'int', 'object': dict(obj)}
        elif obj.default_factory is float:
            return {'factory': 'float', 'object': dict(obj)}

        raise ValueError('Cannot encode a defaultdict with default factory not in (int, float)')

    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        if data['factory'] == 'int':
            return defaultdict(int, data['object'])
        elif data['factory'] == 'float':
            return defaultdict(float, data['object'])

        raise ValueError('Cannot decode a defaultdict with default factory not in (\'int\', \'float\')')


class ComplexDictSerializer(Serializer):
    def can_serialize(self) -> type | tuple[type, ...]:
        return dict

    def encode(self, obj: Any) -> BasicSerializableType:
        return [[key, value] for key, value in obj.items()]

    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        return {default(key): default(value) for key, value in data}


class CopyFieldsSerializer(Serializer):
    def __init__(self, cls: type, fields: tuple[str, ...]) -> None:
        self.cls = cls
        self.fields = fields

    def can_serialize(self) -> type | tuple[type, ...]:
        return self.cls

    def encode(self, obj: Any) -> BasicSerializableType:
        return {field: getattr(obj, field) for field in self.fields}

    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        # noinspection PyArgumentList
        obj = self.cls.__new__(self.cls)

        for field in self.fields:
            object.__setattr__(obj, field, default(data[field]))

        return obj


DEFAULT_SERIALIZERS = [
    TupleSerializer(),
    SetSerializer(),
    DefaultDictSerializer(),
    ComplexDictSerializer(),
]
