from src.database import Database
from src.tournament.interactive_tournament import InteractiveTournamentSerializer, InteractiveTournament, \
    TournamentStateSerializer
from src.tournament.player import PlayerSerializer, Player
from src.tournament.round import RoundSerializer
from src.tournament.round_stats import RoundStatsSerializer
from src.tournament.tournament import TournamentSerializer

SERIALIZERS = [
    PlayerSerializer(),
    InteractiveTournamentSerializer(),
    TournamentSerializer(),
    RoundSerializer(),
    RoundStatsSerializer(),
    TournamentStateSerializer(),
]

# sample test code
def main():
    global_database = Database('database.tmp', *SERIALIZERS)

    data = {
        'players': [
            Player('Adam', 'A'),
            Player('Bob', 'B', 1200),
            Player('Charles', 'C', 1100),
            Player('David', 'D'),
            Player('Eve', 'E'),
            Player('Fred', 'F', 700),
            Player('Jack', 'J', 800),
        ],
        'tournaments': [
            InteractiveTournament()
        ],
        'settings': {}
    }

    it = data['tournaments'][0]

    [it.add_player(p) for p in data['players']]

    it.next_round(pairs=(
        (0, 1),
        (2, 3),
        (4, 5),
    ))

    print('paused:', it.get_round_stats().paused)

    it.set_result(0, (1, 0))
    it.set_result(1, (1, 0))
    it.set_result(2, (.5, .5))

    it.finish()

    print('points:', it.get_round_stats().points)

    global_database.write(data)
    red = global_database.read()
    print('\n\n', red)


if __name__ == '__main__':
    main()
