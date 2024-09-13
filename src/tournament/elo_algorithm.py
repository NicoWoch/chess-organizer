def probability_of_winning(rating1: float, rating2: float) -> float:
    return 1 / (1 + pow(10, (rating2 - rating1) / 400))


def elo_rating_change(rating_a: float, rating_b: float, white_points: float, k: float) -> tuple[float, float]:
    pa = probability_of_winning(rating_a, rating_b)
    pb = probability_of_winning(rating_b, rating_a)

    rating_a_change = k * (white_points - pa)
    rating_b_change = k * ((1 - white_points) - pb)

    return rating_a_change, rating_b_change
