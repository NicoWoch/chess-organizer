from dataclasses import dataclass, field


@dataclass(frozen=True)
class Player:
    name: str
    surname: str
    rating: float = field(default=1000, compare=False)

    hash_id: int = field(default=0, kw_only=True)

    def __post_init__(self):
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "surname", self.surname.strip())

    def __repr__(self):
        return f'<{self.name} {self.surname}>'
