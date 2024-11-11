"""Common DTOs for CyberSource REST API."""

from sincpro_payments_sdk.apps.cybersource.domain import LinkSerMMDRequired
from sincpro_payments_sdk.infrastructure.client_api import ApiResponse
from sincpro_payments_sdk.infrastructure.pydantic import BaseModel


class CyberSourceBaseResponse(ApiResponse):
    id: str


class LinkResponse(BaseModel):
    """Link response."""

    href: str
    method: str


def create_merchant_def_map(merchant_defined_data: LinkSerMMDRequired) -> list[dict]:
    """Create a map of merchant defined data."""
    format_merchant_defined_data = list()
    for key, value in merchant_defined_data.model_dump().items():
        last_word = key.split("_")[-1]
        format_merchant_defined_data.append({"key": last_word, "value": value})
    return format_merchant_defined_data
