from datetime import datetime
from math import exp

from .attempt import Attempt


class EloRating:
    """
    This class represents a single rating for the Elo rating system.
    """

    #: The value of the rating.
    value: float
    #: The timestamp of the rating.
    timestamp: datetime

    def __init__(self, value: float, timestamp: datetime) -> None:
        """
        Initliaze the Elo rating with a value and a timestamp.

        Parameters
        ----------
        value : float
            The value of the rating.
        timestamp : datetime
            The timestamp of the rating.
        """
        self.value = value
        self.timestamp = timestamp


class Elo:
    """
    This class represents the basic Elo rating system with a fixed K-factor.
    It has methods to calculate the update to the rating of a user and a resource.
    Source of algorithm: https://doi.org/10.48550/arXiv.1910.12581
    """

    # Default values:
    #: The default value of a rating.
    default_rating_value: float

    # Hyperparamters:
    #: The starting user weight.
    starting_user_weight: float
    #: The influence on the slope.
    influence_on_slope: float
    #: The weight of a resource.
    resource_weigth: float
    #: The sensitivity of the rating system.
    sensitivity: float

    # Outcomes:
    #: The expected and actual outcomes of the rating system.
    outcomes: dict[str, list[float]] = {"expected_outcomes": [], "actual_outcomes": []}

    def __init__(
        self,
        default_rating_value: float = 0.0,
        starting_user_weight: float = 1.8,
        influence_on_slope: float = 0.05,
        sensitivity: float = 0.4
    ) -> None:
        """
        Initialize the Elo rating system with the default value and hyperparameters.

        Parameters
        ----------
        default_rating_value : float = 0.0
            The default value of a rating.
        starting_user_weight : float = 1.8
            The starting user weight.
        influence_on_slope : float = 0.05
            The influence on the slope.
        sensitivity : float = 0.4
            The sensitivity of the rating system.
        """
        self.default_rating_value = default_rating_value
        self.starting_user_weight = starting_user_weight
        self.influence_on_slope = influence_on_slope
        self.sensitivity = sensitivity

    def calculate_updated_ratings(
        self,
        attempt: Attempt,
        resource_rating: EloRating,
        user_rating: EloRating,
    ) -> dict[str, EloRating]:
        """
        Calculate the updated ratings of a user and a resource.

        Parameters
        ----------
        attempt : Attempt
            The attempt to calculate the updated ratings for.
        resource_rating : EloRating
            The current rating of the resource.
        user_rating : EloRating
            The current rating of the user on the concept of the resource.

        Returns
        -------
        dict[str, EloRating]
            The updated ratings of the user and the resource.
        """
        return {
            "user_rating": self.calculate_updated_user_rating(
                attempt=attempt,
                user_rating=user_rating,
                resource_rating=resource_rating,
            ),
            "resource_rating": self.calculate_updated_resource_rating(
                attempt=attempt,
                user_rating=user_rating,
                resource_rating=resource_rating,
            ),
        }

    def calculate_updated_user_rating(
        self,
        attempt: Attempt,
        user_rating: EloRating,
        resource_rating: EloRating,
    ) -> EloRating:
        """
        Calculate the updated rating of a user.

        Parameters
        ----------
        attempt : Attempt
            The attempt to calculate the updated rating for.
        user_rating : EloRating
            The current rating of the user on the concept of the resource.
        resource_rating : EloRating
            The current rating of the resource.

        Returns
        -------
        EloRating
            The updated rating of the user.
        """
        expected_outcome = self.calculate_expected_outcome(
            user_rating.value, resource_rating.value
        )

        self.outcomes["expected_outcomes"].append(expected_outcome)
        self.outcomes["actual_outcomes"].append(float(attempt.is_attempt_correct))

        return EloRating(
            value=self.calculate_new_user_rating(
                rating_value=user_rating.value,
                expected_outcome=expected_outcome,
                actual_outcome=float(attempt.is_attempt_correct),
            ),
            timestamp=attempt.timestamp,
        )

    def calculate_new_user_rating(
        self,
        rating_value: float,
        expected_outcome: float,
        actual_outcome: float,
    ) -> float:
        """
        Calculate the new rating of a user.

        Parameters
        ----------
        rating_value : float
            The current rating of the user.
        expected_outcome : float
            The outcome that is expected from the user.
        actual_outcome : float
            The actual answer of the user.

        Returns
        -------
        float
            The new rating of the user.
        """
        return rating_value + self.sensitivity * (actual_outcome - expected_outcome)

    def calculate_updated_resource_rating(
        self,
        attempt: Attempt,
        user_rating: EloRating,
        resource_rating: EloRating
    ) -> EloRating:
        """
        Calculate the updated rating of a resource.

        Parameters
        ----------
        attempt : Attempt
            The attempt to calculate the updated rating for.
        user_rating : EloRating
            The current rating of the user on the concept of the resource.
        resource_rating : EloRating
            The current rating of the resource.

        Returns
        -------
        EloRating
            The updated rating of the resource.
        """
        expected_outcome = self.calculate_expected_outcome(
            user_rating_value=user_rating.value,
            resource_rating_value=resource_rating.value,
        )

        return EloRating(
            value=self.calculate_new_resource_rating(
                rating_value=resource_rating.value,
                expected_outcome=expected_outcome,
                actual_outcome=float(attempt.is_attempt_correct),
            ),
            timestamp=attempt.timestamp,
        )

    def calculate_new_resource_rating(
        self,
        rating_value: float,
        expected_outcome: float,
        actual_outcome: float,
    ) -> float:
        """
        Calculate the new rating of a resource.

        Parameters
        ----------
        rating_value : float
            The current rating of the resource.
        expected_outcome : float
            The outcome that is expected from the user.
        actual_outcome : float
            The actual answer of the user.

        Returns
        -------
        float
            The new rating of the resource.
        """
        return rating_value + self.sensitivity * (expected_outcome - actual_outcome)

    def calculate_expected_outcome(
        self,
        user_rating_value: float,
        resource_rating_value: float,
    ) -> float:
        """
        Calculate the expected outcome of a user.

        Parameters
        ----------
        user_rating_value : float
            The rating value of the user.
        resource_rating_value : float
            The rating value of the resource.

        Returns
        -------
        float
            The outcome that is expected from the user.
        """
        return 1 / (1 + exp(-1 * (user_rating_value - resource_rating_value)))