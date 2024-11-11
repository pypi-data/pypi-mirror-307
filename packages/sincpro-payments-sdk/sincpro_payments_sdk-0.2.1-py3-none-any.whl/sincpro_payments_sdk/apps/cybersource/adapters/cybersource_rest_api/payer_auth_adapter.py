"""Payer Auth API adapter."""

from typing import Literal

from sincpro_payments_sdk.apps.cybersource.domain import (
    CardMonthOrDay,
    CardNumber,
    CardType,
    CardYear4Digits,
    LinkSerMMDRequired,
)
from sincpro_payments_sdk.infrastructure.client_api import ClientAPI

# isort: off
from sincpro_payments_sdk.apps.cybersource.infrastructure import (
    CyberSourceAuth,
    get_credential,
)
from .common import CyberSourceBaseResponse, create_merchant_def_map

# isort: on


class SetupAuthenticationResponse(CyberSourceBaseResponse):
    client_ref_info: str
    access_token: str
    device_data_collection_url: str
    reference_id: str
    token: str
    status: Literal["COMPLETED", "FAILED"]


class AuthenticationResponse(CyberSourceBaseResponse):
    status: Literal[
        "AUTHENTICATION_SUCCESSFUL", "PENDING_AUTHENTICATION", "PENDING_AUTHENTICATION"
    ]
    auth_transaction_id: str
    client_ref_info: str
    cavv: str | None = None
    challenge_required: str | None = None
    access_token: str | None = None
    step_up_url: str | None = None
    token: str | None = None


class PayerAuthenticationAdapter(ClientAPI):
    """Adapter for CyberSource Payer Authentication API requests.

    Steps to execute the process Payer Authentication:
        - Setup Payer Authentication
        - Authenticate Enrollment
        - Validate Authentication
    """

    ROUTE_SETUP_PAYER_AUTH = "/risk/v1/authentication-setups"
    ROUTE_AUTH_ENROLLMENT = "/risk/v1/authentications"
    ROUTE_VALIDATE_AUTH = "/risk/v1/authentication-results"

    def __init__(self):
        """Initialize with a CyberSource client."""
        self.ssl = "https://"
        self.host = "apitest.cybersource.com"
        super().__init__(self.base_url, auth=CyberSourceAuth(get_credential()))

    @property
    def base_url(self):
        """Get the base URL for the CyberSource API."""
        return f"{self.ssl}{self.host}"

    def setup_payer_auth(
        self,
        card_number: CardNumber,
        month: CardMonthOrDay,
        year: CardYear4Digits,
        card_type: CardType,
        transaction_ref: str,
    ) -> SetupAuthenticationResponse:
        """Setup Payer Authentication with CyberSource."""
        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "paymentInformation": {
                "card": {
                    "type": card_type,
                    "expirationMonth": month,
                    "expirationYear": year,
                    "number": card_number,
                }
            },
        }

        response = self.execute_request(
            self.ROUTE_SETUP_PAYER_AUTH,
            "POST",
            data=payload,
        )
        dict_response = response.json()
        if "errorInformation" in dict_response:
            raise Exception(str(dict_response["errorInformation"]))

        return SetupAuthenticationResponse(
            raw_response=dict_response,
            id=dict_response.get("id"),
            client_ref_info=dict_response["clientReferenceInformation"]["code"],
            access_token=dict_response["consumerAuthenticationInformation"]["accessToken"],
            device_data_collection_url=dict_response["consumerAuthenticationInformation"][
                "deviceDataCollectionUrl"
            ],
            reference_id=dict_response["consumerAuthenticationInformation"]["referenceId"],
            token=dict_response["consumerAuthenticationInformation"]["token"],
            status=dict_response.get("status"),
        )

    def auth_enrollment(
        self,
        card_number: CardNumber,
        month: CardMonthOrDay,
        year: CardYear4Digits,
        card_type: CardType,
        transaction_ref: str,
        reference_id: str,
        amount: str | float,
        currency: str,
        linkser_merchant_def: LinkSerMMDRequired | None = None,
    ) -> AuthenticationResponse:
        """Authenticate enrollment with CyberSource."""
        payload = {
            "paymentInformation": {
                "card": {
                    "type": card_type,
                    "expirationMonth": month,
                    "expirationYear": year,
                    "number": card_number,
                }
            },
            "clientReferenceInformation": {"code": transaction_ref},
            "consumerAuthenticationInformation": {
                "referenceId": reference_id,
                "deviceChannel": "Browser",
            },
            "orderInformation": {
                "amountDetails": {
                    "totalAmount": amount,
                    "currency": currency,
                },
            },
        }

        if linkser_merchant_def:
            payload["merchantDefinedInformation"] = create_merchant_def_map(
                linkser_merchant_def
            )

        response = self.execute_request(
            self.ROUTE_AUTH_ENROLLMENT,
            "POST",
            data=payload,
        )
        dict_response = response.json()

        return AuthenticationResponse(
            raw_response=dict_response,
            id=dict_response.get("id"),
            status=dict_response.get("status"),
            auth_transaction_id=dict_response["consumerAuthenticationInformation"][
                "authenticationTransactionId"
            ],
            client_ref_info=dict_response["clientReferenceInformation"]["code"],
            cavv=dict_response["consumerAuthenticationInformation"].get("cavv", None),
            challenge_required=dict_response["consumerAuthenticationInformation"].get(
                "challengeRequired", None
            ),
            access_token=dict_response["consumerAuthenticationInformation"].get(
                "accessToken", None
            ),
            step_up_url=dict_response["consumerAuthenticationInformation"].get(
                "stepUpUrl", None
            ),
            token=dict_response["consumerAuthenticationInformation"].get("token", None),
        )

    def validate_auth(
        self,
        card_number: CardNumber,
        month: CardMonthOrDay,
        year: CardMonthOrDay,
        card_type: CardType,
        auth_transaction_id: str,
        amount: str | float,
        currency: str,
    ) -> AuthenticationResponse:
        """Validate authentication with CyberSource."""
        response = self.execute_request(
            self.ROUTE_AUTH_ENROLLMENT,
            "POST",
            data={
                "paymentInformation": {
                    "card": {
                        "type": card_type,
                        "expirationMonth": month,
                        "expirationYear": year,
                        "number": card_number,
                    }
                },
                "consumerAuthenticationInformation": {
                    "authenticationTransactionId": auth_transaction_id
                },
                "orderInformation": {
                    "amountDetails": {
                        "totalAmount": amount,
                        "currency": currency,
                    },
                },
            },
        )

        dict_response = response.json()
        if "errorInformation" in dict_response:
            raise Exception(str(dict_response["errorInformation"]))

        return AuthenticationResponse(
            raw_response=dict_response,
            id=dict_response.get("id"),
            status=dict_response.get("status"),
            auth_transaction_id=dict_response["consumerAuthenticationInformation"][
                "authenticationTransactionId"
            ],
            client_ref_info=dict_response["clientReferenceInformation"]["code"],
        )
