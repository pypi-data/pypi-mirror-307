"""Card domain module."""

from enum import StrEnum
from typing import NewType

from sincpro_payments_sdk.infrastructure.domain import new_value_object
from sincpro_payments_sdk.infrastructure.pydantic import BaseModel


def validate_card_size(value: str):
    if len(value) != 16:
        raise ValueError("Card number must have 16 digits.")


def validate_cvv_size(value: str):
    """Check if the CVV is valid."""
    if len(value) != 3:
        raise ValueError("CVV must have 3 digits.")


def validate_month_or_day_size(month_or_day: str) -> None:
    """Check if the month and year are valid."""
    if len(month_or_day) < 2:
        raise ValueError("Month and year must have at least 2 digits")


def validate_year_size(year: str) -> None:
    """Check if the year is valid."""
    if len(year) != 4:
        raise ValueError("Year must have 4 digits")


# Value objects
CardNumber = new_value_object(NewType("CardNumber", str), validate_card_size)

CardCVV = new_value_object(NewType("CardCVV", str), validate_cvv_size)

CardMonthOrDay = new_value_object(
    NewType("CardDateAttribute", str), validate_month_or_day_size
)

CardYear4Digits = new_value_object(
    NewType("CardYear4Digits", str), validate_month_or_day_size
)


class CardType(StrEnum):
    """Card type enumeration."""

    VISA = "001"
    MASTERCARD = "002"


class Card(BaseModel):
    card_type: CardType
    card_number: CardNumber
    month: CardMonthOrDay
    year: CardYear4Digits
    cvv: CardCVV
