"""Tokenization adapter for CyberSource REST API."""

# isort: off
from sincpro_payments_sdk.apps.cybersource.infrastructure import (
    CyberSourceAuth,
    get_credential,
)

# isort: on

from sincpro_payments_sdk.apps.cybersource.domain import (
    CardMonthOrDay,
    CardNumber,
    CardType,
    CardYear4Digits,
)
from sincpro_payments_sdk.infrastructure.client_api import ClientAPI


class TokenizationAdapter(ClientAPI):
    """Adapter for CyberSource Tokenization API requests."""

    ROUTE_INSTRUMENT_IDENTIFICATION = "/tms/v1/instrumentidentifiers"
    ROUTE_PAYMENT_INSTRUMENTS = "/tms/v1/paymentinstruments"
    ROUTE_CUSTOMERS = "/tms/v2/customers"
    ROUTE_CUSTOMER_PAYMENT_INSTRUMENTS = "/tms/v2/customers/{customerId}/payment-instruments"

    def __init__(self):
        """Initialize with a CyberSource client."""
        self.ssl = "https://"
        self.host = "apitest.cybersource.com"
        super().__init__(self.base_url, auth=CyberSourceAuth(get_credential()))

    @property
    def base_url(self):
        """Get the base URL for the CyberSource API."""
        return f"{self.ssl}{self.host}"

    def create_card(self, card_number: CardNumber) -> dict:
        """Tokenize a credit card with CyberSource."""

        body = {
            "card": {
                "number": card_number,
            },
        }

        response = self.execute_request(
            self.ROUTE_INSTRUMENT_IDENTIFICATION, "POST", data=body
        )

        return response.json()

    def create_card_payment_method(
        self,
        tokenized_card_id: str,
        month: CardMonthOrDay,
        year: CardYear4Digits,
        card_type: str,
    ) -> dict:
        """Tokenize a credit card with CyberSource."""
        body = {
            "card": {"expirationMonth": month, "expirationYear": year, "type": card_type},
            "instrumentIdentifier": {"id": tokenized_card_id},
        }

        response = self.execute_request(
            self.ROUTE_PAYMENT_INSTRUMENTS,
            "POST",
            data=body,
        )
        return response.json()

    def create_customer(self, external_id: str, email: str) -> dict:
        """Create a customer in CyberSource as token."""
        payload = {
            "buyerInformation": {
                "merchantCustomerID": external_id,
                "email": email,
            },
            "clientReferenceInformation": {"code": external_id},
        }
        response = self.execute_request(
            self.ROUTE_CUSTOMERS,
            data=payload,
        )
        return response.json()

    def associate_card_payment_method_to_customer(
        self,
        tokenized_customer_id: str,
        tokenized_card_id: str,
        month: CardMonthOrDay,
        year: CardYear4Digits,
        card_type: CardType,
    ):
        """Create a card and add it to a customer.
        it is known as customer payment instrument in Cybersource playform
        """
        payload = {
            "card": {"expirationMonth": month, "expirationYear": year, "type": card_type},
            "instrumentIdentifier": {"id": tokenized_card_id},
        }
        response = self.execute_request(
            self.ROUTE_CUSTOMER_PAYMENT_INSTRUMENTS.format(customerId=tokenized_customer_id),
            data=payload,
        )
        return response.json()

    def list_customer_payment_methods(self, tokenized_customer_id: str):
        """List all cards associated with a customer."""
        response = self.execute_request(
            self.ROUTE_CUSTOMER_PAYMENT_INSTRUMENTS.format(customerId=tokenized_customer_id),
            "GET",
        )
        return response.json()
