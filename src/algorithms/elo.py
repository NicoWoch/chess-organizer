from src.config import Config


def probability(rating1: int, rating2: int) -> float:
    return 1 / (1 + pow(10, (rating2 - rating1) / 400))


def elo_rating(rating_a: int, rating_b: int, white_points: float, k=Config.ELO_K_VALUE) -> tuple[int, int]:
    pa = probability(rating_a, rating_b)
    pb = probability(rating_b, rating_a)

    rating_a += k * (white_points - pa)
    rating_b += k * ((1 - white_points) - pb)

    return round(rating_a), round(rating_b)
