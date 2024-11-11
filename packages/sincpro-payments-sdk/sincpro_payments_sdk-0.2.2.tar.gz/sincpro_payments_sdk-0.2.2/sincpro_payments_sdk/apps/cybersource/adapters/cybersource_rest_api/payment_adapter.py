"""CyberSource Adapter Module"""

from typing import Literal

from sincpro_payments_sdk.apps.cybersource.domain.payments import (
    CaptureState,
    LinkSerMMDRequired,
    PayAuthState,
)
from sincpro_payments_sdk.infrastructure.client_api import ClientAPI

# isort: off
from sincpro_payments_sdk.apps.cybersource.infrastructure import (
    CyberSourceAuth,
    get_credential,
)

# isort: on

from sincpro_payments_sdk.apps.cybersource.domain import (
    BillingInformation,
    Card,
    CurrencyType,
)

from .common import CyberSourceBaseResponse, LinkResponse, create_merchant_def_map


class PaymentAuthorizationApiResponse(CyberSourceBaseResponse):
    """Payment authorization response."""

    status: PayAuthState
    order_information: dict
    link_payment_auth: LinkResponse
    link_payment_capture: LinkResponse
    link_reverse_auth: LinkResponse


class ReverseAuthApiResponse(CyberSourceBaseResponse):
    """Reverse authorization response."""

    status: Literal["REVERSED",]


class PaymentCaptureApiResponse(CyberSourceBaseResponse):
    """Payment capture response."""

    status: CaptureState | PayAuthState
    order_information: dict
    link_payment_capture: LinkResponse
    link_void: LinkResponse


class RefundPaymentApiResponse(CyberSourceBaseResponse):
    """Refund payment response."""

    status: str
    order_information: dict
    link_refund: LinkResponse
    link_void: LinkResponse


class RefundCaptureApiResponse(CyberSourceBaseResponse):
    """Refund capture response."""

    status: str
    order_information: dict
    link_capture_refund: LinkResponse
    link_void_capture: LinkResponse


class PaymentAdapter(ClientAPI):
    """Adapter for CyberSource Payment API requests.

    Step:
    - Payment Authorization
      - Check Payment Status
      - Payment Capture | OR | Payment Auth Reverse
    - Payment Capture Success
      - Payment Void
    - Payment Refund
      - Payment Refund Capture
    """

    ROUTE_AUTH_PAYMENTS = "/pts/v2/payments"
    ROUTE_AUTH_PAYMENT = "/pts/v2/payments/{id}"
    ROUTE_REVERSE_AUTH = "/pts/v2/payments/{id}/reversals"
    ROUTE_PAYMENT_CAPTURE = "/pts/v2/payments/{id}/captures"
    ROUTE_REFUND_PAYMENT = "/pts/v2/payments/{id}/refunds"
    ROUTE_REFUND_CAPTURE = "/pts/v2/captures/{id}/refunds"
    ROUTE_CAPTURE = "/pts/v2/captures/{id}"
    ROUTE_CHECK_STATUS_PAYMENT = "/pts/v2/refresh-payment-status/{id}"

    def __init__(self):
        """Initialize with a CyberSource client."""
        self.ssl = "https://"
        self.host = "apitest.cybersource.com"
        super().__init__(self.base_url, auth=CyberSourceAuth(get_credential()))

    @property
    def base_url(self):
        """Get the base URL for the CyberSource API."""
        return f"{self.ssl}{self.host}"

    def direct_payment(
        self,
        transaction_ref: str,
        card: Card | None,
        token_id: str | None,
        amount: float,
        currency: CurrencyType,
        billing_info: BillingInformation,
        merchant_defined_data: LinkSerMMDRequired,
        transaction_session_id: str,
        auth_transaction_id: str | None = None,
        cavv: str | None = None,
    ) -> PaymentCaptureApiResponse:
        """Direct payment with CyberSource.
        - Authorize payment
        - Capture payment
        in One Step
        """
        format_merchant_defined_data = create_merchant_def_map(merchant_defined_data)

        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "paymentInformation": dict(),
            "orderInformation": {
                "amountDetails": {"totalAmount": str(amount), "currency": currency},
                "billTo": {
                    "firstName": billing_info.first_name,
                    "lastName": billing_info.last_name,
                    "address1": billing_info.address,
                    "locality": billing_info.city_name,
                    "administrativeArea": billing_info.city_code,
                    "postalCode": billing_info.postal_code,
                    "country": billing_info.country_code,
                    "email": billing_info.email,
                    "phoneNumber": billing_info.phone,
                },
            },
            "merchantDefinedInformation": format_merchant_defined_data,
            "deviceInformation": {"fingerprintSessionId": transaction_session_id},
            "processingInformation": {"capture": True},
        }

        if token_id and not card:
            payload["paymentInformation"]["paymentInstrument"] = {"id": token_id}

        if card and not token_id:
            payload["paymentInformation"]["card"] = {
                "number": card.card_number,
                "expirationMonth": card.month,
                "expirationYear": card.year,
                "type": card.card_type,
                "securityCode": card.cvv,
            }

        if auth_transaction_id or cavv:
            payload["consumerAuthenticationInformation"] = dict()

        if auth_transaction_id:
            payload["consumerAuthenticationInformation"]["authenticationTransactionId"] = (
                auth_transaction_id,
            )
        if cavv:
            payload["consumerAuthenticationInformation"]["cavv"] = cavv

        response = self.execute_request(
            self.ROUTE_AUTH_PAYMENTS,
            "POST",
            data=payload,
        )
        res_py_obj = response.json()

        return PaymentCaptureApiResponse(
            id=res_py_obj["id"],
            status=res_py_obj["status"],
            order_information=res_py_obj["orderInformation"],
            link_payment_capture=LinkResponse(**res_py_obj["_links"]["self"]),
            link_void=LinkResponse(**res_py_obj["_links"]["void"]),
            raw_response=res_py_obj,
        )

    def payment_authorization(
        self,
        transaction_ref: str,
        card: Card | None,
        token_id: str | None,
        amount: float,
        currency: CurrencyType,
        billing_info: BillingInformation,
        merchant_defined_data: LinkSerMMDRequired,
        transaction_session_id: str,
        auth_transaction_id: str | None = None,
        cavv: str | None = None,
    ) -> PaymentAuthorizationApiResponse:
        """Create a payment Auth with CyberSource()."""
        format_merchant_defined_data = create_merchant_def_map(merchant_defined_data)

        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "paymentInformation": dict(),
            "orderInformation": {
                "amountDetails": {"totalAmount": str(amount), "currency": currency},
                "billTo": {
                    "firstName": billing_info.first_name,
                    "lastName": billing_info.last_name,
                    "address1": billing_info.address,
                    "locality": billing_info.city_name,
                    "administrativeArea": billing_info.city_code,
                    "postalCode": billing_info.postal_code,
                    "country": billing_info.country_code,
                    "email": billing_info.email,
                    "phoneNumber": billing_info.phone,
                },
            },
            "merchantDefinedData": format_merchant_defined_data,
            "deviceInformation": {"fingerprintSessionId": transaction_session_id},
        }

        if token_id and not card:
            payload["paymentInformation"]["paymentInstrument"] = {"id": token_id}

        if card and not token_id:
            payload["paymentInformation"]["card"] = {
                "number": card.card_number,
                "expirationMonth": card.month,
                "expirationYear": card.year,
                "type": card.card_type,
                "securityCode": card.cvv,
            }

        if auth_transaction_id or cavv:
            payload["consumerAuthenticationInformation"] = dict()

        if auth_transaction_id:
            payload["consumerAuthenticationInformation"]["authenticationTransactionId"] = (
                auth_transaction_id,
            )
        if cavv:
            payload["consumerAuthenticationInformation"]["cavv"] = cavv

        response = self.execute_request(
            self.ROUTE_AUTH_PAYMENTS,
            "POST",
            data=payload,
        )
        res_py_obj = response.json()
        return PaymentAuthorizationApiResponse(
            id=res_py_obj["id"],
            status=res_py_obj["status"],
            order_information=res_py_obj["orderInformation"],
            link_payment_auth=LinkResponse(**res_py_obj["_links"]["self"]),
            link_payment_capture=LinkResponse(**res_py_obj["_links"]["capture"]),
            link_reverse_auth=LinkResponse(**res_py_obj["_links"]["authReversal"]),
            raw_response=res_py_obj,
        )

    def get_auth_payment(self, payment_id: str) -> CyberSourceBaseResponse:
        """Check the status of a payment."""
        response = self.execute_request(
            self.ROUTE_AUTH_PAYMENT.format(id=payment_id),
            "GET",
        )
        res_py_obj = response.json()
        return CyberSourceBaseResponse(id=res_py_obj["id"], raw_response=res_py_obj)

    def reverse_auth_payment(
        self,
        payment_id: str,
        reason: str,
        transaction_ref: str,
        amount: float,
        currency: CurrencyType,
    ) -> ReverseAuthApiResponse:
        """Reverse a payment authorization with CyberSource."""
        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "orderInformation": {
                "amountDetails": {"totalAmount": str(amount), "currency": currency}
            },
            "reason": reason,
        }
        response = self.execute_request(
            self.ROUTE_REVERSE_AUTH.format(id=payment_id),
            "POST",
            data=payload,
        )
        res_py_obj = response.json()

        return ReverseAuthApiResponse(
            id=res_py_obj["id"],
            status=res_py_obj["status"],
            raw_response=res_py_obj,
        )

    def capture_payment(
        self, payment_id: str, transaction_ref: str, amount: float, currency: CurrencyType
    ) -> PaymentCaptureApiResponse:
        """Capture a payment with CyberSource."""

        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "orderInformation": {
                "amountDetails": {"totalAmount": str(amount), "currency": currency}
            },
        }
        response = self.execute_request(
            self.ROUTE_PAYMENT_CAPTURE.format(id=payment_id),
            method="POST",
            data=payload,
        )
        res_py_obj = response.json()
        return PaymentCaptureApiResponse(
            id=res_py_obj["id"],
            status=res_py_obj["status"],
            order_information=res_py_obj["orderInformation"],
            link_payment_capture=LinkResponse(**res_py_obj["_links"]["self"]),
            link_void=LinkResponse(**res_py_obj["_links"]["void"]),
            raw_response=res_py_obj,
        )

    def get_capture_payment(self, capture_id: str) -> CyberSourceBaseResponse:
        """Get Metadata of capture payment."""
        res = self.execute_request(
            self.ROUTE_CAPTURE.format(id=capture_id),
            method="GET",
        )
        res_py_obj = res.json()
        return CyberSourceBaseResponse(id=res_py_obj["id"], raw_response=res_py_obj)

    def refund_payment(
        self, capture_id: str, transaction_ref: str, amount: float, currency: CurrencyType
    ) -> RefundPaymentApiResponse:
        """Refund

        :param capture_id: Capture Payment ID
        :param transaction_ref: Reference of the transaction from external service
        :param amount:
        :param currency:
        :return:
        """
        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "orderInformation": {
                "amountDetails": {"totalAmount": str(amount), "currency": currency}
            },
        }
        response = self.execute_request(
            self.ROUTE_REFUND_PAYMENT.format(id=capture_id),
            method="POST",
            data=payload,
        )
        res_py_obj = response.json()
        return RefundPaymentApiResponse(
            id=res_py_obj["id"],
            status=res_py_obj["status"],
            order_information=res_py_obj["orderInformation"],
            link_refund=LinkResponse(**res_py_obj["_links"]["self"]),
            link_void=LinkResponse(**res_py_obj["_links"]["void"]),
            raw_response=res_py_obj,
        )

    def capture_refund(
        self,
        capture_payment_id: str,
        transaction_ref: str,
        amount: float,
        currency: CurrencyType,
    ) -> RefundCaptureApiResponse:
        """Capture a refund."""
        payload = {
            "clientReferenceInformation": {"code": transaction_ref},
            "orderInformation": {
                "amountDetails": {"totalAmount": str(amount), "currency": currency}
            },
        }
        response = self.execute_request(
            self.ROUTE_REFUND_CAPTURE.format(id=capture_payment_id),
            "POST",
            data=payload,
        )
        res_py_obj = response.json()
        return RefundCaptureApiResponse(
            raw_response=res_py_obj,
            id=res_py_obj["id"],
            status=res_py_obj["status"],
            order_information=res_py_obj["orderInformation"],
            link_capture_refund=LinkResponse(**res_py_obj["_links"]["self"]),
            link_void_capture=LinkResponse(**res_py_obj["_links"]["void"]),
        )
