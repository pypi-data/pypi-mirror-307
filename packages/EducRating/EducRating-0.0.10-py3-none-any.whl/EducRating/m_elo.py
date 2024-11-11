from datetime import datetime
from math import exp

from .attempt import Attempt


class MEloRating:
    """
    This class represents a single rating for the M-Elo rating system.
    """

    #: The value of the rating.
    value: float
    #: The timestamp of the rating.
    timestamp: datetime

    def __init__(self, value: float, timestamp: datetime):
        """
        Initialize the M-Elo rating with a value and a timestamp.

        Parameters
        ----------
        value : float
            The value of the rating.
        timestamp : datetime
            The timestamp of the rating.
        """
        self.value = value
        self.timestamp = timestamp


class MElo:
    """
    This class represents the M-Elo rating system.
    It has methods to calculate the update to the rating of a user and a resource.
    Source of algorithm: https://doi.org/10.48550/arXiv.1910.12581
    """

    # Default values:
    #: The default value of a rating.
    default_rating_value: float

    # Hyperparameters:
    #: The starting value of the sensitivity.
    starting_value: float
    #: The slope of changes.
    slope_of_changes: float

    # Outcomes:
    #: The expected and actual outcomes of the rating system.
    outcomes: dict[str, list[float]] = {"expected_outcomes": [], "actual_outcomes": []}

    def __init__(
        self,
        default_rating_value: float = 0.0,
        starting_value: float = 1.8,
        slope_of_changes: float = 0.05,
    ):
        """
        Initialize the M-Elo rating system with the default value and hyperparameters.

        Parameters
        ----------
        default_rating_value : float = 0.0
            The default value of a rating.
        starting_value : float = 1.8
            The starting value of the sensitivity.
        slope_of_changes : float = 0.05
            The slope of changes.
        """
        self.default_rating_value = default_rating_value
        self.starting_value = starting_value
        self.slope_of_changes = slope_of_changes

    def calculate_updated_ratings(
        self,
        attempt: Attempt,
        user_rating: MEloRating,
        resource_rating: MEloRating,
        all_user_ratings_on_concept_of_resource: list[MEloRating],
        prior_user_rating_update_count: int,
        prior_resource_rating_update_count: int,
    ) -> dict[str, MEloRating]:
        """
        Calculate the updated ratings of a user and a resource.

        Parameters
        ----------
        attempt : Attempt
            The attempt made by the user.
        user_rating : MEloRating
            The rating of the user on the concept of the resource.
        resource_rating : MEloRating
            The rating of the resource.
        all_user_ratings_on_concept_of_resource : list[MEloRating]
            The ratings of all users on the concept of the resource.
        prior_user_rating_update_count : int
            The number of times the user rating was updated before.
        prior_resource_rating_update_count : int
            The number of times the resource rating was updated before.

        Returns
        -------
        dict[str, MEloRating]
            The updated ratings of the user and the resource.
        """
        return {
            "user_rating": self.calculate_updated_user_rating(
                attempt=attempt,
                user_rating=user_rating,
                resource_rating=resource_rating,
                prior_rating_update_count=prior_user_rating_update_count,
                all_user_ratings_on_concepts=all_user_ratings_on_concept_of_resource,
            ),
            "resource_rating": self.calculate_updated_resource_rating(
                all_user_ratings_on_concepts=all_user_ratings_on_concept_of_resource,
                attempt=attempt,
                resource_rating=resource_rating,
                prior_rating_update_count=prior_resource_rating_update_count,
            ),
        }

    def calculate_updated_user_rating(
        self,
        attempt: Attempt,
        user_rating: MEloRating,
        resource_rating: MEloRating,
        prior_rating_update_count: int,
        all_user_ratings_on_concepts: list[MEloRating],
    ) -> MEloRating:
        """
        Calculate the updated rating of a user.

        Parameters
        ----------
        attempt : Attempt
            The attempt made by the user.
        user_rating : MEloRating
            The rating of the user on the concept of the resource.
        resource_rating : MEloRating
            The rating of the resource.
        prior_rating_update_count : int
            The number of times the user rating was updated before.
        all_user_ratings_on_concepts : list[MEloRating]
            The ratings of all users on the concept of the resource.

        Returns
        -------
        MEloRating
            The updated rating of the user.
        """
        sensitivity = self.calculate_sensitivity(
            prior_rating_update_count=prior_rating_update_count
        )

        average_user_rating_on_concepts: float = (
            self.calculate_average_user_rating_value(
                user_ratings=all_user_ratings_on_concepts
            )
        )

        average_expected_outcome: float = self.calculate_expected_outcome(
            rating_value_a=average_user_rating_on_concepts,
            rating_value_b=resource_rating.value,
        )

        normalization_denominator: float = self.calculate_normalization_denominator(
            actual_outcome=float(attempt.is_attempt_correct),
            all_user_ratings_on_concepts=all_user_ratings_on_concepts,
            resource_rating=resource_rating,
        )

        normalization_factor: float = self.calculate_normalization_factor(
            actual_outcome=float(attempt.is_attempt_correct),
            normalization_denominator=normalization_denominator,
            average_expected_outcome=average_expected_outcome,
        )

        expected_outcome: float = self.calculate_expected_outcome(
            rating_value_a=user_rating.value,
            rating_value_b=resource_rating.value,
        )

        self.outcomes["expected_outcomes"].append(average_expected_outcome)
        self.outcomes["actual_outcomes"].append(float(attempt.is_attempt_correct))

        return MEloRating(
            value=self.calculate_new_user_rating_value(
                user_rating=user_rating,
                normalization_factor=normalization_factor,
                sensitivity=sensitivity,
                actual_outcome=float(attempt.is_attempt_correct),
                expected_outcome=expected_outcome,
            ),
            timestamp=attempt.timestamp,
        )

    def calculate_new_user_rating_value(
        self,
        user_rating: MEloRating,
        normalization_factor: float,
        sensitivity: float,
        actual_outcome: float,
        expected_outcome: float,
    ) -> float:
        """
        Calculate the new rating of a user.

        Parameters
        ----------
        user_rating : MEloRating
            The rating of the user.
        normalization_factor : float
            The normalization factor.
        sensitivity : float
            The sensitivity of the rating system.
        actual_outcome : float
            The answer of the user.
        expected_outcome : float
            The outcome that is expected from the user.

        Returns
        -------
        float
            The new rating of the user.
        """
        return user_rating.value + normalization_factor * sensitivity * (
            actual_outcome - expected_outcome
        )

    def calculate_updated_resource_rating(
        self,
        all_user_ratings_on_concepts: list[MEloRating],
        attempt: Attempt,
        resource_rating: MEloRating,
        prior_rating_update_count: int,
    ) -> MEloRating:
        """
        Calculate the updated rating of a resource.

        Parameters
        ----------
        all_user_ratings_on_concepts : list[MEloRating]
            The ratings of all users on the concept of the resource.
        attempt : Attempt
            The attempt made by the user.
        resource_rating : MEloRating
            The rating of the resource.
        prior_rating_update_count : int
            The number of times the resource rating was updated before.

        Returns
        -------
        MEloRating
            The updated rating of the resource.
        """
        sensitivity: float = self.calculate_sensitivity(
            prior_rating_update_count=prior_rating_update_count
        )

        average_user_rating_on_concepts = self.calculate_average_user_rating_value(
            user_ratings=all_user_ratings_on_concepts
        )

        expected_outcome: float = self.calculate_expected_outcome(
            rating_value_a=average_user_rating_on_concepts,
            rating_value_b=resource_rating.value,
        )

        return MEloRating(
            value=self.calculate_new_resource_rating_value(
                resource_rating=resource_rating,
                sensitivity=sensitivity,
                expected_outcome=expected_outcome,
                actual_outcome=float(attempt.is_attempt_correct),
            ),
            timestamp=attempt.timestamp,
        )

    def calculate_new_resource_rating_value(
        self,
        resource_rating: MEloRating,
        sensitivity: float,
        expected_outcome: float,
        actual_outcome: float,
    ) -> float:
        """
        Calculate the new rating of a resource.

        Parameters
        ----------
        resource_rating : MEloRating
            The rating of the resource.
        sensitivity : float
            The sensitivity of the rating system.
        expected_outcome : float
            The outcome that is expected from the user.
        actual_outcome : float
            The actual answer of the user.

        Returns
        -------
        int
            The new rating of the resource.
        """
        return resource_rating.value + sensitivity * (expected_outcome - actual_outcome)

    def calculate_sensitivity(self, prior_rating_update_count: int) -> float:
        """
        Calculate the sensitivity.

        Parameters
        ----------
        prior_rating_update_count : int
            The number of times the rating was updated before.

        Returns
        -------
        float
            The sensitivity of the rating system.
        """
        return self.starting_value / (
            1 + self.slope_of_changes * prior_rating_update_count
        )

    def calculate_average_user_rating_value(
        self, user_ratings: list[MEloRating]
    ) -> float:
        """
        Calculate the average user rating value.

        Parameters
        ----------
        user_ratings : list[MEloRating]
            A list of user ratings.

        Returns
        -------
        float
            The average user rating value.
        """
        if len(user_ratings) == 0:
            raise ValueError("The list of user ratings is empty.")

        return sum([user_rating.value for user_rating in user_ratings]) / len(
            user_ratings
        )

    def calculate_expected_outcome(
        self, rating_value_a: float, rating_value_b: float
    ) -> float:
        """
        Calculate the expected outcome.

        Parameters
        ----------
        rating_value_a : float
            The first rating value.
        rating_value_b : float
            The second rating value.

        Returns
        -------
        float
            The expected outcome.
        """
        return 1 / (1 + exp(-1 * (rating_value_a - rating_value_b)))

    def calculate_normalization_denominator(
        self,
        actual_outcome: float,
        all_user_ratings_on_concepts: list[MEloRating],
        resource_rating: MEloRating,
    ) -> float:
        """
        Calculate the denominator for the normalization factor.

        Parameters
        ----------
        actual_outcome : float
            The actual answer of the user.
        all_user_ratings_on_concepts : list[MEloRating]
            The ratings of all users on the concept of the resource.
        resource_rating : MEloRating
            The rating of the resource.

        Returns
        -------
        float
            The normalization denominator.
        """
        if len(all_user_ratings_on_concepts) == 0:
            return abs(actual_outcome)

        normalization_denominator: float = 0.0

        for user_rating in all_user_ratings_on_concepts:
            normalization_denominator += abs(
                actual_outcome
                - self.calculate_expected_outcome(
                    rating_value_a=user_rating.value,
                    rating_value_b=resource_rating.value,
                )
                * (1 / len(all_user_ratings_on_concepts))
            )
        return normalization_denominator

    def calculate_normalization_factor(
        self,
        average_expected_outcome: float,
        actual_outcome: float,
        normalization_denominator: float,
    ) -> float:
        """
        Calculate the normalization factor.

        Parameters
        ----------
        average_expected_outcome : float
            The average expected outcome.
        actual_outcome : float
            The actual answer of the user.
        normalization_denominator : float
            The normalization denominator.

        Returns
        -------
        float
            The normalization factor.
        """
        return (
            abs(average_expected_outcome - actual_outcome) / normalization_denominator
        )
