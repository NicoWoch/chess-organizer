from dataclasses import dataclass

from src.serializer import CopyFieldsSerializer


@dataclass(init=False)
class Player:
    name: str
    surname: str
    rating: float

    def __init__(self, name: str, surname: str, rating : float = 1000):
        self.name = name
        self.surname = surname
        self.rating = rating


class PlayerSerializer(CopyFieldsSerializer):
    def __init__(self):
        super().__init__(Player, (
            'name',
            'surname',
            'rating',
        ))
