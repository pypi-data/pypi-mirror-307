class ChoiceError(Exception):
    """Base class for exceptions in this module."""

    pass


class DuplicateChoiceError(ChoiceError):
    """Raised when attempting to add a duplicate choice."""

    pass


class InvalidChoiceCodeError(ChoiceError):
    """Raised when an invalid choice code is used."""

    pass


class InvalidChoicesResponseError(Exception):
    """Raised when a choices response string is invalid."""

    pass
