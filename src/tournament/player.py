from dataclasses import dataclass, field


@dataclass(frozen=True, order=False)
class Player:
    name: str
    rating: float = field(default=1000)

    hash_id: int = field(default=0, kw_only=True)

    def __post_init__(self):
        object.__setattr__(self, "name", ' '.join(self.name.split()))

    def __repr__(self):
        return f'<{self.name}({self.rating})>'

    def __eq__(self, other):
        return self.name == other.name and self.hash_id == other.hash_id

    def __lt__(self, other):
        if self.name == other.name:
            return self.rating < other.rating

        name_rev = ' '.join(self.name.split()[::-1])
        other_name_rev = ' '.join(self.name.split()[::-1])

        return name_rev < other_name_rev
