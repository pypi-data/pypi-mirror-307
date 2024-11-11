"""Domain module for Cybersource credentials."""

from sincpro_payments_sdk.infrastructure.pydantic import BaseModel


class CybersourceCredential(BaseModel):
    """Base class for Cybersource credentials."""

    key_id: str
    secret_key: str
    merchant_id: str
    profile_id: str | None = None
