from functools import wraps
from typing import Callable, Any


def tk_validator(validator: Callable) -> Callable[..., dict[str, Any]]:
    @wraps(validator)
    def wrapper(self, **kwargs):
        vcmd = self.register(lambda text: validator(self, text, **kwargs))

        return {
            'validate': 'all',
            'validatecommand': (vcmd, '%P'),
        }

    return wrapper


@tk_validator
def tk_unsigned_validator(_, text: str):
    return text.isdigit()


@tk_validator
def tk_unsigned_float_validator(_, text: str):
    return text.replace('.', '', 1).isdigit()
