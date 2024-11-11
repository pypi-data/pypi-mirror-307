from datetime import datetime

from src.EducRating.attempt import Attempt
from src.EducRating.elo_with_uncertainty import EloWithUncertainty, EloRating


def test_elo_rating() -> None:
    elo_rating = EloRating(value=0, timestamp=datetime.now())
    assert elo_rating.value == 0
    assert isinstance(elo_rating.timestamp, datetime)


def test_elo() -> None:
    elo = EloWithUncertainty()
    assert elo.default_rating_value == 0
    assert elo.starting_user_weight > 1.7
    assert elo.starting_user_weight < 1.9
    assert elo.influence_on_slope > 0.04
    assert elo.influence_on_slope < 0.06
    result = elo.calculate_updated_ratings(
        Attempt(
            attempt_id=0,
            user_id="test",
            resource_id="test",
            concept_id="test",
            timestamp=datetime.now(),
            is_attempt_correct=True,
        ),
        EloRating(value=0, timestamp=datetime.now()),
        EloRating(value=0, timestamp=datetime.now()),
        0,
        0,
    )
    assert isinstance(result, dict)
    assert isinstance(result["user_rating"], EloRating)
    assert isinstance(result["user_rating"].value, float)
    assert result["user_rating"].value < 1.0
    assert result["user_rating"].value > 0.8
    assert isinstance(result["resource_rating"], EloRating)
    assert isinstance(result["resource_rating"].value, float)
    assert result["resource_rating"].value < -0.8
    assert result["resource_rating"].value > -1.0
    uncertainty = elo.calculate_uncertainty(1)
    assert isinstance(uncertainty, float)
    assert uncertainty < 1.8
    assert uncertainty > 1.7
