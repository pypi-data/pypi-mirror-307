from datetime import datetime

from src.EducRating.attempt import Attempt


def test_attempt() -> None:
    attempt = Attempt(
        attempt_id="1",
        user_id="1",
        resource_id="1",
        concept_id="1",
        timestamp=datetime.now(),
        is_attempt_correct=True,
    )
    assert attempt.attempt_id == "1"
    assert attempt.user_id == "1"
    assert attempt.resource_id == "1"
    assert attempt.concept_id == "1"
    assert isinstance(attempt.timestamp, datetime)
    assert attempt.is_attempt_correct is True
