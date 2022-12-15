import random

from src.algorithms.swiss_tournament import SwissTournament
from src.player import Gender, Player

NAMES_M = '''Jan
Andrzej
Piotr
Krzysztof
Stanisław
Tomasz
Paweł
Józef
Marcin
Marek
Michał
Grzegorz
Jerzy
Tadeusz
Adam
Łukasz
Zbigniew
Ryszard
Dariusz
Henryk
Mariusz
Kazimierz
Wojciech
Robert
Mateusz
Marian
Rafał
Jacek
Janusz
Mirosław
Maciej
Sławomir
Jarosław
Kamil
Wiesław
Roman
Władysław
Jakub
Artur
Zdzisław
Edward
Mieczysław
Damian
Dawid
Przemysław
Sebastian
Czesław
Leszek
Daniel
Waldemar'''.split('\n')

NAMES_F = '''Anna
Maria
Katarzyna
Małgorzata
Agnieszka
Krystyna
Barbara
Ewa
Elżbieta
Zofia
Janina
Teresa
Joanna
Magdalena
Monika
Jadwiga
Danuta
Irena
Halina
Helena
Beata
Aleksandra
Marta
Dorota
Marianna
Grażyna
Jolanta
Stanisława
Iwona
Karolina
Bożena
Urszula
Justyna
Renata
Alicja
Paulina
Sylwia
Natalia
Wanda
Agata
Aneta
Izabela
Ewelina
Marzena
Wiesława
Genowefa
Patrycja
Kazimiera
Edyta
Stefania'''.split('\n')

SURNAMES = '''Nowak
Kowalski
Wiśniewski
Dąbrowski
Lewandowski
Wójcik
Kamiński
Kowalczyk
Zieliński
Szymański
Woźniak
Kozłowski
Jankowski
Wojciechowski
Kwiatkowski
Kaczmarek
Mazur
Krawczyk
Piotrowski
Grabowski
Nowakowski
Pawłowski
Michalski
Nowicki
Adamczyk
Dudek
Zając
Wieczorek
Jabłoński
Król
Majewski
Olszewski
Jaworski
Wróbel
Malinowski
Pawlak
Witkowski
Walczak
Stępień
Górski
Rutkowski
Michalak
Sikora
Ostrowski
Baran
Duda
Szewczyk
Tomaszewski
Pietrzak
Marciniak
Wróblewski
Zalewski
Jakubowski
Jasiński
Zawadzki
Sadowski
Bąk
Chmielewski
Włodarczyk
Borkowski
Czarnecki
Sawicki
Sokołowski
Urbański
Kubiak
Maciejewski
Szczepański
Kucharski
Wilk
Kalinowski
Lis
Mazurek
Wysocki
Adamski
Kaźmierczak
Wasilewski
Sobczak
Czerwiński
Andrzejewski
Cieślak
Głowacki
Zakrzewski
Kołodziej
Sikorski
Krajewski
Gajewski
Szymczak
Szulc
Baranowski
Laskowski
Brzeziński
Makowski
Ziółkowski
Przybylski'''.split('\n')


def get_random_player(rng=None):
    if rng is None:
        rng = random.Random()

    gender = rng.choice(
        [Gender.Men, Gender.Women] * 5 + [Gender.Other]
    )

    if gender == Gender.Men:
        name = rng.choice(NAMES_M)
    elif gender == Gender.Women:
        name = rng.choice(NAMES_F)
    else:
        name = rng.choice(NAMES_M + NAMES_F)

    surname = rng.choice(SURNAMES)
    rating = rng.randint(500, 2000)

    return Player.create_player(name=name, surname=surname, gender=gender, rating=rating)


def get_random_players(count, rng=None):
    return [get_random_player(rng) for _ in range(count)]


def create_empty_tournament(id_):
    return SwissTournament(f'Testowy turniej id={id_}')
