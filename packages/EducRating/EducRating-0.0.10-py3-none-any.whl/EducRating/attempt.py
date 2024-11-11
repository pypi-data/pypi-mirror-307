from datetime import datetime


class Attempt:
    """
    This class represents an attempt made by an user on a resource.
    """

    #: The id of the attempt.
    attempt_id: str
    #: The id of the user that made the attempt.
    user_id: str
    #: The id of the resource the attempt was made on.
    resource_id: str
    #: The id of the course the resource is associated with.
    concept_id: str
    #: The time the attempt was made.
    timestamp: datetime
    #: Whether the attempt was correct or not.
    is_attempt_correct: bool

    def __init__(
        self,
        attempt_id: str,
        user_id: str,
        resource_id: str,
        concept_id: str,
        timestamp: datetime,
        is_attempt_correct: bool,
    ):
        """
        Initializes an Attempt.

        Parameters
        ----------
        attempt_id : str
            The id of the attempt.
        user_id : str
            The id of the user that made the attempt.
        resource_id : str
            The id of the resource the attempt was made on.
        concept_id : str
            The id of the course the resource is associated with.
        timestamp : datetime
            The time the attempt was made.
        is_attempt_correct : bool
            Whether the attempt was correct or not.
        """

        self.attempt_id = attempt_id
        self.user_id = user_id
        self.resource_id = resource_id
        self.concept_id = concept_id
        self.timestamp = timestamp
        self.is_attempt_correct = is_attempt_correct
