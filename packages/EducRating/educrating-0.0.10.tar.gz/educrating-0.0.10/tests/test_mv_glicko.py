from datetime import datetime

from src.EducRating.attempt import Attempt
from src.EducRating.mv_glicko import MVGlicko, MVGlickoRating


def test_mv_glicko_rating() -> None:
    mv_glicko_rating = MVGlickoRating(
        value=1500, deviation=350, timestamp=datetime.now()
    )
    assert mv_glicko_rating.value == 1500
    assert mv_glicko_rating.deviation == 350
    assert isinstance(mv_glicko_rating.timestamp, datetime)


def test_mv_glicko() -> None:
    mv_glicko = MVGlicko()
    assert mv_glicko.default_rating_value == 1500
    assert mv_glicko.default_rating_deviation == 350
    assert mv_glicko.increase_in_variance == 50
    assert mv_glicko.minimal_amount_of_updates == 10
    assert mv_glicko.sensitivity_of_estimations < 0.9
    assert mv_glicko.sensitivity_of_estimations > 0.7
    result = mv_glicko.calculate_updated_ratings(
        Attempt(
            attempt_id=0,
            user_id="test",
            resource_id="test",
            concept_id="test",
            timestamp=datetime.now(),
            is_attempt_correct=True,
        ),
        MVGlickoRating(value=1500, deviation=350, timestamp=datetime.now()),
        MVGlickoRating(value=1500, deviation=350, timestamp=datetime.now()),
        [MVGlickoRating(value=1500, deviation=350, timestamp=datetime.now())],
    )
    assert isinstance(result, dict)
    assert isinstance(result["user_rating"], MVGlickoRating)
    assert isinstance(result["user_rating"].value, float)
    assert result["user_rating"].value > 1629
    assert result["user_rating"].value < 1630
    assert result["user_rating"].deviation > 290
    assert result["user_rating"].deviation < 291
    assert isinstance(result["resource_rating"], MVGlickoRating)
    assert isinstance(result["resource_rating"].value, float)
    assert result["resource_rating"].value > 1337
    assert result["resource_rating"].value < 1338
    assert result["resource_rating"].deviation > 290
    assert result["resource_rating"].deviation < 291

    deviation_over_time = mv_glicko.calculate_user_rating_deviation_over_time_passage(
        500.0, datetime.now() - datetime.now()
    )
    assert deviation_over_time > 349.9
    assert deviation_over_time < 350.1

    user_rating_value = mv_glicko.calculate_new_user_rating_value(
        False, 1500.0, 1.0, 1.0
    )
    assert user_rating_value > 1498.9
    assert user_rating_value < 1499.1

    try:
        mv_glicko.calculate_average_user_rating_value([])
    except ValueError:
        pass

    try:
        mv_glicko.calculate_average_user_rating_deviation([])
    except ValueError:
        pass
    
    result = mv_glicko.calculate_updated_user_rating(
        Attempt(
            attempt_id=0,
            user_id="test",
            resource_id="test",
            concept_id="test",
            timestamp=datetime.now(),
            is_attempt_correct=True,
        ),
        MVGlickoRating(value=1500, deviation=350, timestamp=datetime.now()),
        MVGlickoRating(value=1500, deviation=350, timestamp=datetime.now()),
        [],
    )

    assert mv_glicko.outcomes == {'actual_outcomes': [1.0, 1.0], 'expected_outcomes': [0.5]}