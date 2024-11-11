"""Customer domain model."""

from pydantic import Field

from sincpro_payments_sdk.infrastructure.pydantic import BaseModel


class BillingInformation(BaseModel):
    """Billing information."""

    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city_name: str
    city_code: str
    country_code: str
    postal_code: str


class Customer(BaseModel):
    """General customer information."""

    id: str
    external_id: str
    name: str
    email: str
    payment_method: list[str] = Field(default_factory=list)
    default_billing_information: BillingInformation | None

    def has_billing_information(self) -> bool:
        return self.default_billing_information is not None
