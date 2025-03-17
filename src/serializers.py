import json
from datetime import datetime
from typing import Any

from src.algorithms.constants import Result
from src.algorithms.tournament import Tournament
from src.player import Player


def _serialize_datetime(date: datetime) -> dict:
    return {
        '__datetime__': True,
        'time': date.timestamp()
    }


def _deserialize_datetime(dct: dict) -> datetime | dict:
    if '__datetime__' not in dct or dct['__datetime__'] is not True:
        return dct

    return datetime.fromtimestamp(dct['time'])


def _serialize_player(player: Player) -> dict:
    last_played = None if player.last_played is None else _serialize_datetime(player.last_played)
    ratings_history = [(_serialize_datetime(t), rating) for t, rating in player.get_rating_history()]

    return {
        '__player__': True,
        'name': player.name,
        'surname': player.surname,
        'creation_date': _serialize_datetime(player.creation_date),
        'last_played': last_played,
        'ratings_history': ratings_history,
    }


def _deserialize_player(dct: dict) -> Player | dict:
    if '__player__' not in dct or dct['__player__'] is not True:
        return dct

    ratings_history = [(date, rating) for date, rating in dct['ratings_history']]

    return Player(
        _name=dct['name'],
        _surname=dct['surname'],
        creation_date=dct['creation_date'],
        last_played=dct['last_played'],
        _ratings_history=ratings_history,
    )


def _serialize_result(result: Result) -> dict:
    dct = {'__result__': True}

    if result == Result.Black:
        dct['value'] = 'black'
    elif result == Result.White:
        dct['value'] = 'white'
    elif result == Result.Draw:
        dct['value'] = 'draw'
    else:
        dct['value'] = '-'

    return dct


def _deserialize_result(dct: dict) -> Result | dict:
    if '__result__' not in dct or dct['__result__'] is not True:
        return dct

    if dct['value'] == 'black':
        return Result.Black
    elif dct['value'] == 'white':
        return Result.White
    elif dct['value'] == 'draw':
        return Result.Draw

    return Result.Playing


def _serialize_tournament(tournament: Tournament) -> dict:
    rounds: list[list[tuple[int, int, Result]]] = [
        [
            (game.white, game.black, game.result)
            for game in games
        ]
        for games in tournament.rounds
    ]

    return {
        '__tournament__': True,
        'name': tournament.name,
        'started_date': tournament.started_date,
        'pairer': 'Swiss',                  # TODO
        'players': tournament.players,
        'rounds': rounds,
        'ratings_at_start': getattr(tournament, '_ratings_at_start'),
        'ratings_at_end': getattr(tournament, '_ratings_at_end'),
        'is_finished': tournament.is_finished,
    }


def _deserialize_tournament(dct: dict) -> Tournament | dict:
    if '__tournament__' not in dct or dct['__tournament__'] is not True:
        return dct



    return dct  # TODO


def serializer_hook(obj: Any) -> dict:
    if isinstance(obj, datetime):
        return _serialize_datetime(obj)
    elif isinstance(obj, Player):
        return _serialize_player(obj)
    elif isinstance(obj, Result):
        return _serialize_result(obj)
    elif isinstance(obj, Tournament):
        return _serialize_tournament(obj)

    raise TypeError(f'Cannot serialize type \"{type(obj)}\"')


def deserializer_hook(dct: dict) -> Any:
    funcs = (
        _deserialize_datetime, _deserialize_player,
        _deserialize_result, _deserialize_tournament
    )

    for func in funcs:
        if not isinstance(dct, dict):
            return dct

        dct = func(dct)

    return dct
