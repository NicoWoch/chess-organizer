# <center>chess-organizer</center>

---

## App Structure:
- *dist*
- *src*
  - *algorithms*
    - swiss_algorithm.py
  - *objects*
    - player.py
    - round.py
    - tournament.py
  - organizer.kv
  - main.py
- *tests*
  - *algorithms*
    - test_swiss_algorithm.py
  - *objects*
    - test_player.py
    - test_round.py
    - test.tournament.py
- readme.md

---

### player.py:
- Player dataclass:
  - *variables:*
    - name : str
    - surname : str
    - rating : int
    - tournament-stats : dict
      > tournament-stats will be used to store big and small point
        of a player in swiss game while on tournament
- *global functions:*
  - load_players(file_path: str) -> List[Player]
    > Should load players from JSON file given

---

### round.py:
- Enum Result: WIN, DRAW, LOST
- class Round:
  - *variables:*
    - games : List[Tuple[Player]]
    - results : List[int]
    - algorithm : Module
  - *functions:*
    - \_\_init\_\_(games, algorithm)
    - set_result(game_id: int, result: Result)
    - end_round()
      > Ending a round should calculate all ratings and
        update players object accordingly

---

### tournament.py:
- class Tournament:
  - *variables:*
    - players : List[Players]
    - rounds : List[Round]
    - algorithm : Module
  - *functions:*
    - \_\_init\_\_(players, algorithm)
    - set_result(game_id: int, result: Result)
    - start_round()
    - finish_round()
    - get_ranking() -> List[Players]
      > Execute algorithm.get_ranking with last round

---

### swiss_algorithm.py:
- *functions:*
  - init_players(players: List[Player])
    > Setting default values for big and small points
  - open_round(players: List[Round]) -> Round
    > Choosing which players to pair which and making round object of it
  - close_round(round: Round)
    > Updating rating, big and small points of players
  - get_ranking(round: Round) -> List[Player] # Sorted
    > Return players ordered by their tournament points

---
