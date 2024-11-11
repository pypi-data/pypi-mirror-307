from datetime import datetime

from src.EducRating.attempt import Attempt
from src.EducRating.m_elo import MElo, MEloRating


def test_m_elo_rating() -> None:
    m_elo_rating = MEloRating(value=0, timestamp=datetime.now())
    assert m_elo_rating.value == 0
    assert isinstance(m_elo_rating.timestamp, datetime)


def test_m_elo() -> None:
    m_elo = MElo()
    assert m_elo.default_rating_value == 0
    assert m_elo.starting_value > 1.7
    assert m_elo.starting_value < 1.9
    assert m_elo.slope_of_changes > 0.04
    assert m_elo.slope_of_changes < 0.06
    result = m_elo.calculate_updated_ratings(
        Attempt(
            attempt_id=0,
            user_id="test",
            resource_id="test",
            concept_id="test",
            timestamp=datetime.now(),
            is_attempt_correct=True,
        ),
        MEloRating(value=0, timestamp=datetime.now()),
        MEloRating(value=0, timestamp=datetime.now()),
        [MEloRating(value=0, timestamp=datetime.now())],
        0,
        0,
    )
    assert isinstance(result, dict)
    assert isinstance(result["user_rating"], MEloRating)
    assert isinstance(result["user_rating"].value, float)
    assert result["user_rating"].value > 0.8
    assert result["user_rating"].value < 1.0
    assert isinstance(result["resource_rating"], MEloRating)
    assert isinstance(result["resource_rating"].value, float)
    assert result["resource_rating"].value > -1.0
    assert result["resource_rating"].value < -0.8
    normalization_denominator = m_elo.calculate_normalization_denominator(
        1.0,
        [],
        MEloRating(value=0.0, timestamp=datetime.now()),
    )
    assert isinstance(normalization_denominator, float)
    assert normalization_denominator < 1.1
    assert normalization_denominator > 0.9

    try:
        m_elo.calculate_average_user_rating_value([])
    except ValueError:
        pass
