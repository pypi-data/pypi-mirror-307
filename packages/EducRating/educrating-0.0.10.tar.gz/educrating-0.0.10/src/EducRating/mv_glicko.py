from datetime import datetime, timedelta
from math import log, pi, pow, sqrt
from sys import maxsize

from .attempt import Attempt


class MVGlickoRating:
    """
    This class represents a single rating for the MV-Glicko rating system.
    """

    #: The value of the rating.
    value: float
    #: The deviation of the rating.
    deviation: float
    #: The timestamp of the rating.
    timestamp: datetime

    def __init__(self, value: float, deviation: float, timestamp: datetime) -> None:
        """
        Initialize the MV-Glicko rating with a value, a deviation, and a timestamp.

        Parameters
        ----------
        value : float
            The value of the rating.
        deviation : float
            The deviation of the rating.
        timestamp : datetime
            The timestamp of the rating.
        """
        self.value = value
        self.deviation = deviation
        self.timestamp = timestamp


class MVGlicko:
    """
    This class represents the MV-Glicko rating system.
    It has methods to calculate the update to the rating of a user and a resource.
    Source of algorithm: https://doi.org/10.1145/3448139.3448189
    """

    # Default values:
    #: The default value of a rating.
    default_rating_value: float
    #: The default deviation of a rating.
    default_rating_deviation: float

    # Hyperparameters:
    #: The increase in variance.
    increase_in_variance: int
    #: The minimal amount of updates.
    minimal_amount_of_updates: int
    #: The sensitivity of the estimations.
    sensitivity_of_estimations: float

    # Constants:
    #: The value to standardize the logistic function.
    standardize_logistic_function_value: float = log(10) / 400

    # Outcomes:
    #: The expected and actual outcomes of the rating system.
    outcomes: dict[str, list[float]] = {"expected_outcomes": [], "actual_outcomes": []}

    def __init__(
        self,
        default_rating_value: float = 1500.0,
        default_rating_deviation: float = 350.0,
        increase_in_variance: int = 50,
        minimal_amount_of_updates: int = 10,
        sensitivity_of_estimations: float = 0.8,
    ) -> None:
        """
        Initialize MV-Glicko rating system with default values and hyperparameters.

        Parameters
        ----------
        default_rating_value : float = 1500.0
            The default value of a rating.
        default_rating_deviation : float = 350.0
            The default deviation of a rating.
        increase_in_variance : int = 50
            The increase in variance.
        minimal_amount_of_updates : int = 10
            The minimal amount of updates.
        sensitivity_of_estimations : float = 0.8
            The sensitivity of the estimations.
        """
        self.default_rating_value = default_rating_value
        self.default_rating_deviation = default_rating_deviation
        self.increase_in_variance = increase_in_variance
        self.minimal_amount_of_updates = minimal_amount_of_updates
        self.sensitivity_of_estimations = sensitivity_of_estimations

    def calculate_updated_ratings(
        self,
        attempt: Attempt,
        resource_rating: MVGlickoRating,
        user_rating: MVGlickoRating,
        all_user_ratings_of_user_on_concepts_of_resource: list[MVGlickoRating],
    ) -> dict[str, MVGlickoRating]:
        """
        Execute MV-Glicko algorithm and calculate the updated ratings.

        Parameters
        ----------
        attempt : Attempt
            The attempt made by the user.
        resource_rating : MVGlickoRating
            The current rating of the resource.
        user_rating : MVGlickoRating
            The current rating of the user on the concept of the resource.
        all_user_ratings_of_user_on_concepts_of_resource : list[MVGlickoRating]
            The current ratings of the user on all concepts of the resource.

        Returns
        -------
        dict[str, MVGlickoRating]
            The updated ratings of the user and the resource.
        """
        return {
            "user_rating": self.calculate_updated_user_rating(
                attempt=attempt,
                user_rating=user_rating,
                resource_rating=resource_rating,
                all_user_ratings_of_user_on_concepts_of_resource=all_user_ratings_of_user_on_concepts_of_resource,
            ),
            "resource_rating": self.calculate_updated_resource_rating(
                attempt=attempt,
                resource_rating=resource_rating,
                all_user_ratings_of_user_on_concepts_of_resource=all_user_ratings_of_user_on_concepts_of_resource,
            ),
        }

    def calculate_updated_user_rating(
        self,
        attempt: Attempt,
        user_rating: MVGlickoRating,
        resource_rating: MVGlickoRating,
        all_user_ratings_of_user_on_concepts_of_resource: list[MVGlickoRating] = [],
    ) -> MVGlickoRating:
        """
        Calculate the updated rating of a user.

        Parameters
        ----------
        attempt : Attempt
            The attempt made by the user on the concept of the resource.
        user_rating : MVGlickoRating
            The current rating of the user.
        resource_rating : MVGlickoRating
            The current rating of the resource.
        all_user_ratings_of_user_on_concepts_of_resource : list[MVGlickoRating] = []
            The current ratings of the user on all concepts of the resource.

        Returns
        -------
        MVGlickoRating
            The updated rating of the user.
        """
        # Calculate the time difference between the current and last interaction of a user.
        time_delta: timedelta = attempt.timestamp - user_rating.timestamp

        # If the time difference is less than one hour, the passage of time is not included in the calculation.
        user_rating_deviation_over_time_passage = (
            self.calculate_user_rating_deviation_over_time_passage(
                user_rating_deviation=user_rating.deviation, time_delta=time_delta
            )
            if time_delta.total_seconds() > 3600
            else user_rating.deviation
        )

        reduced_impact = self.calculate_reduced_impact(
            rating_deviation=resource_rating.deviation,
        )

        expected_outcome = self.calculate_expected_outcome(
            reduced_impact=reduced_impact,
            rating_value_a=user_rating.value,
            rating_value_b=resource_rating.value,
        )

        self.outcomes["actual_outcomes"].append(float(attempt.is_attempt_correct))

        if(len(all_user_ratings_of_user_on_concepts_of_resource) > 0):
            # Calculate the average user rating value of a user on all concepts of the resource.
            average_user_rating_value_of_user_on_concepts_of_resource = (
                self.calculate_average_user_rating_value(
                    user_ratings=all_user_ratings_of_user_on_concepts_of_resource
                )
            )

            expected_outcome_of_user = self.calculate_expected_outcome(
                reduced_impact=reduced_impact,
                rating_value_a=average_user_rating_value_of_user_on_concepts_of_resource,
                rating_value_b=resource_rating.value,
            )

            self.outcomes["expected_outcomes"].append(expected_outcome_of_user)

        delta_inverse_squared = self.calculate_delta_inverse_squared(
            reduced_impact=reduced_impact,
            expected_outcome=expected_outcome,
        )

        amount_of_updates = self.calculate_amount_of_updates(
            rating_deviation=user_rating_deviation_over_time_passage,
            delta_inverse_squared=delta_inverse_squared,
            reduced_impact=reduced_impact,
            minimal_amount_of_updates=self.sensitivity_of_estimations,
        )

        return MVGlickoRating(
            value=self.calculate_new_user_rating_value(
                actual_outcome=attempt.is_attempt_correct,
                user_rating_value=user_rating.value,
                amount_of_updates=amount_of_updates,
                expected_outcome=expected_outcome,
            ),
            deviation=self.calculate_rating_deviation(
                rating_deviation=user_rating_deviation_over_time_passage,
                delta_inverse_squared=delta_inverse_squared,
            ),
            timestamp=attempt.timestamp,
        )

    def calculate_updated_resource_rating(
        self,
        attempt: Attempt,
        resource_rating: MVGlickoRating,
        all_user_ratings_of_user_on_concepts_of_resource: list[MVGlickoRating],
    ) -> MVGlickoRating:
        """
        Calculate the updated rating of a resource.

        Parameters
        ----------
        attempt : Attempt
            The attempt made by the user.
        resource_rating : MVGlickoRating
            The current rating of the resource.
        all_user_ratings_of_user_on_concepts_of_resource : list[MVGlickoRating]
            The current ratings of the user on all concepts of the resource.

        Returns
        -------
        MVGlickoRating
            The updated rating of the resource.
        """

        # Calculate the average resource rating deviation
        average_user_deviation_of_user_on_concepts_of_resource = (
            self.calculate_average_user_rating_deviation(
                user_ratings=all_user_ratings_of_user_on_concepts_of_resource
            )
        )

        reduced_impact = self.calculate_reduced_impact(
            rating_deviation=average_user_deviation_of_user_on_concepts_of_resource,
        )

        # Calculate the average user rating value of a user on all concepts of the resource.
        average_user_rating_value_of_user_on_concepts_of_resource = (
            self.calculate_average_user_rating_value(
                user_ratings=all_user_ratings_of_user_on_concepts_of_resource
            )
        )

        expected_outcome = self.calculate_expected_outcome(
            reduced_impact=reduced_impact,
            rating_value_a=resource_rating.value,
            rating_value_b=average_user_rating_value_of_user_on_concepts_of_resource,
        )

        delta_inverse_squared = self.calculate_delta_inverse_squared(
            reduced_impact=reduced_impact,
            expected_outcome=expected_outcome,
        )

        amount_of_updates = self.calculate_amount_of_updates(
            rating_deviation=resource_rating.deviation,
            delta_inverse_squared=delta_inverse_squared,
            reduced_impact=reduced_impact,
        )

        return MVGlickoRating(
            value=self.calculate_resource_rating_value(
                actual_outcome=attempt.is_attempt_correct,
                resource_rating_value=resource_rating.value,
                amount_of_updates=amount_of_updates,
                expected_outcome=expected_outcome,
            ),
            deviation=self.calculate_rating_deviation(
                rating_deviation=resource_rating.deviation,
                delta_inverse_squared=delta_inverse_squared,
            ),
            timestamp=attempt.timestamp,
        )

    def calculate_user_rating_deviation_over_time_passage(
        self, user_rating_deviation: float, time_delta: timedelta
    ) -> float:
        """
        Calculate the rating deviation of a user over the passage of time.

        Parameters
        ----------
        user_rating_deviation : float
            The current rating deviation of the user.
        time_delta : timedelta
            The time difference between the current and last interaction of a user.

        Returns
        -------
        float
            The rating deviation of a user over the passage of time.
        """
        return min(
            sqrt(
                pow(user_rating_deviation, 2)
                + pow(self.increase_in_variance, 2)
                * (time_delta.total_seconds() / 86400)
            ),
            350.0,
        )

    def calculate_reduced_impact(
        self,
        rating_deviation: float,
    ) -> float:
        """
        Calculate the reduced impact.

        Parameters
        ----------
        rating_deviation : float
            The deviation of a rating.

        Returns
        -------
        float
            The reduced impact.
        """
        return 1 / sqrt(
            1
            + 3
            * pow(self.standardize_logistic_function_value, 2)
            * pow(rating_deviation, 2)
            / pow(pi, 2)
        )

    def calculate_expected_outcome(
        self,
        reduced_impact: float,
        rating_value_a: float,
        rating_value_b: float,
    ) -> float:
        """
        Calculate the expected outcome of attempt on b by a.

        Parameters
        ----------
        reduced_impact : float
            The reduced impact.
        rating_value_a : float
            The first rating value.
        rating_value_b : float
            The second rating value.

        Returns
        -------
        float
            The oucome that is expected from the user.
        """
        return 1 / (
            1
            + pow(
                10,
                -reduced_impact * (rating_value_a - rating_value_b) / 400,
            )
        )

    def calculate_delta_inverse_squared(
        self,
        reduced_impact: float,
        expected_outcome: float,
    ) -> float:
        """
        Calculate the delta inverse squared.

        Parameters
        ----------
        reduced_impact : float
            The reduced impact.
        expected_outcome : float
            The oucome that is expected from the user.

        Returns
        -------
        float
            The delta inverse squared.
        """
        return pow(
            pow(self.standardize_logistic_function_value, 2)
            * pow(reduced_impact, 2)
            * expected_outcome
            * (1 - expected_outcome),
            -1,
        )

    def calculate_amount_of_updates(
        self,
        rating_deviation: float,
        delta_inverse_squared: float,
        reduced_impact: float,
        minimal_amount_of_updates: int = -maxsize - 1,
    ) -> float:
        """
        Calculate the amount of updates.

        Parameters
        ----------
        rating_deviation : float
            The deviation of a rating.
        delta_inverse_squared : float
            The delta inverse squared.
        reduced_impact : float
            The reduced impact.
        minimal_amount_of_updates : int = -maxsize - 1
            The minimal amount of updates.

        Returns
        -------
        float
            The amount of updates.
        """
        return max(
            self.standardize_logistic_function_value
            / (1 / pow(rating_deviation, 2) + 1 / delta_inverse_squared)
            * reduced_impact,
            minimal_amount_of_updates,
        )

    def calculate_new_user_rating_value(
        self,
        actual_outcome: bool,
        user_rating_value: float,
        amount_of_updates: float,
        expected_outcome: float,
    ) -> float:
        """
        Calculate the new rating value of a user.

        Parameters
        ----------
        actual_outcome : bool
            The actual answer of the user.
        user_rating_value : float
            The current rating value of the user.
        amount_of_updates : float
            The amount of updates.
        expected_outcome : float
            The outcome that is expected from the user.

        Returns
        -------
        float
            The new rating value of the user.
        """
        if actual_outcome:
            return (
                user_rating_value
                + amount_of_updates
                * self.sensitivity_of_estimations
                * (int(actual_outcome) - expected_outcome)
            )
        else:
            return user_rating_value + amount_of_updates * (
                int(actual_outcome) - expected_outcome
            )

    def calculate_resource_rating_value(
        self,
        actual_outcome: bool,
        resource_rating_value: float,
        amount_of_updates: float,
        expected_outcome: float,
    ) -> float:
        """
        Calculate the new rating value of a resource.

        Parameters
        ----------
        actual_outcome : bool
            The actual answer of the user.
        resource_rating_value : float
            The current rating value of the resource.
        amount_of_updates : float
            The amount of updates.
        expected_outcome : float
            The outcome that is expected from the user.

        Returns
        -------
        float
            The new rating value of the resource.
        """
        return resource_rating_value + amount_of_updates * (
            int(not actual_outcome) - expected_outcome
        )

    def calculate_rating_deviation(
        self,
        rating_deviation: float,
        delta_inverse_squared: float,
    ) -> float:
        """
        Calculate a new rating deviation.

        Parameters
        ----------
        rating_deviation : float
            The deviation of a rating.
        delta_inverse_squared : float
            The delta inverse squared.

        Returns
        -------
        float
            The new deviation of the rating.
        """
        return pow(
            sqrt(1 / pow(rating_deviation, 2) + 1 / delta_inverse_squared),
            -1,
        )

    def calculate_average_user_rating_value(
        self, user_ratings: list[MVGlickoRating]
    ) -> float:
        """
        Calculate the average user rating value.

        Parameters
        ----------
        user_ratings : list[MVGlickoRating]
            The list of user ratings.

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

    def calculate_average_user_rating_deviation(
        self, user_ratings: list[MVGlickoRating]
    ) -> float:
        """
        Calculate the average user rating deviation.

        Parameters
        ----------
        user_ratings : list[MVGlickoRating]
            The list of user ratings.

        Returns
        -------
        float
            The average user rating deviation.
        """
        if len(user_ratings) == 0:
            raise ValueError("The list of user ratings is empty.")

        return sum([user_rating.deviation for user_rating in user_ratings]) / len(
            user_ratings
        )
