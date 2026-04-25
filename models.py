from typing import TypedDict


class ValidationErrorItem(TypedDict):
    """Represent a single XML validation error."""

    path: str | None
    reason: str | None
    message: str


class ValidationResponse(TypedDict):
    """Represent the standard response returned by the validator."""

    valid: bool
    errors: list[ValidationErrorItem]
    number_errors: int
