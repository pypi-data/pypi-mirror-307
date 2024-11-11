"""Use case to create an anonymous payment in CyberSource."""

from sincpro_payments_sdk.apps.cybersource.domain import (
    ALLOWED_CITY,
    ALLOWED_CITY_CODE,
    ALLOWED_COUNTRY_CODE,
    AmountDetails,
    BillingInformation,
    CurrencyType,
    IndustrySectorOptions,
    LinkSerMMDRequired,
    PayAuthState,
    SourceOptions,
)
from sincpro_payments_sdk.apps.cybersource.use_cases import (
    DataTransferObject,
    Feature,
    cybersource,
)


class CommandDirectPaymentWithToken(DataTransferObject):
    """Data Transfer Object to create an anonymous payment in CyberSource."""

    # Payment info
    token_id: str
    transaction_ref: str
    amount: float
    currency: str
    city_code: str
    city_name: str
    country_code: str

    # Customer infor
    customer_id: str
    customer_firstname: str
    customer_lastname: str
    customer_email: str
    customer_phone: str
    customer_address: str
    customer_postal_code: str

    # LINKSER info CUSTOMER
    is_logged_user: bool
    source_transaction: SourceOptions
    customer_number_document: str

    # LINKSER info COMPANY
    industry_sector: IndustrySectorOptions
    company_number_document: str
    company_name: str
    product_description: str

    # Session id
    transaction_session_id: str

    # Authentication 3D
    auth_transaction_id: str | None = None
    cavv: str | None = None


class ResponseDirectPaymentWithToken(DataTransferObject):
    payment_id: str
    capture_id: str | None
    link_get_auth_payment: str | None
    link_get_capture_payment: str | None
    link_void_payment: str | None
    raw_response_auth: dict | None = None
    raw_response_capture: dict | None = None


@cybersource.feature(CommandDirectPaymentWithToken)
class DirectPaymentWithToken(Feature):
    """
    Create an anonymous payment in CyberSource.
    """

    def execute(self, dto: CommandDirectPaymentWithToken) -> ResponseDirectPaymentWithToken:
        """Main execution"""
        self.validate_country_and_city(dto)

        # 1 Billing
        billing_info = BillingInformation(
            first_name=dto.customer_firstname,
            last_name=dto.customer_lastname,
            email=dto.customer_email,
            phone=dto.customer_phone,
            address=dto.customer_address,
            city_code=dto.city_code,
            city_name=dto.city_name,
            postal_code=dto.customer_postal_code,
            country_code=dto.country_code,
        )

        # 2 Amount
        amount = AmountDetails(
            total_amount=dto.amount,
            currency=CurrencyType(dto.currency),
        )

        # Required by LINKSER
        merchant_defined_data = LinkSerMMDRequired(
            merchant_defined_data_1="SI" if dto.is_logged_user else "NO",
            merchant_defined_data_7=f"{dto.customer_firstname} {dto.customer_lastname}",
            merchant_defined_data_9=dto.source_transaction,
            merchant_defined_data_11=dto.customer_number_document,
            merchant_defined_data_12=dto.customer_phone,
            merchant_defined_data_14=dto.industry_sector,
            merchant_defined_data_15=dto.company_number_document,
            merchant_defined_data_87=dto.company_number_document,
            merchant_defined_data_88=dto.company_name,
            merchant_defined_data_90=dto.product_description,
        )

        return self._execute_one_request(
            dto,
            dto.token_id,
            amount,
            billing_info,
            merchant_defined_data,
            dto.auth_transaction_id,
            dto.cavv,
        )

        # return self._execute_payment_with_capture(
        #     dto, card, amount, billing_info, merchant_defined_data
        # )

    def _execute_one_request(
        self,
        dto: CommandDirectPaymentWithToken,
        token: str,
        amount: AmountDetails,
        billing_info: BillingInformation,
        merchant_defined_data: LinkSerMMDRequired,
        auth_transaction_id: str,
        cavv: str,
    ):
        direct_payment = self.payment_adapter.direct_payment(
            dto.transaction_ref,
            None,
            token,
            amount.total_amount,
            amount.currency,
            billing_info,
            merchant_defined_data,
            dto.transaction_session_id,
            auth_transaction_id,
            cavv,
        )

        if direct_payment.status in [PayAuthState.DECLINED, PayAuthState.INVALID_REQUEST]:
            raise Exception("Payment authorization failed")

        return ResponseDirectPaymentWithToken(
            payment_id=direct_payment.id,
            capture_id=None,
            link_get_auth_payment=None,
            link_void_payment=direct_payment.link_void.href,
            link_get_capture_payment=None,
            raw_response_auth=direct_payment.raw_response,
            raw_response_capture=None,
        )

    @staticmethod
    def validate_country_and_city(dto: CommandDirectPaymentWithToken):
        """Validate country and city."""
        if dto.country_code not in ALLOWED_COUNTRY_CODE:
            raise Exception(
                f"The value {dto.country_code=} not allowed in {ALLOWED_COUNTRY_CODE=}"
            )
        if dto.city_code not in ALLOWED_CITY_CODE:
            raise Exception(f"The value {dto.city_code=} not allowed in {ALLOWED_CITY_CODE=}")
        if dto.city_name not in ALLOWED_CITY:
            raise Exception(f"The value {dto.city_name=} not allowed in {ALLOWED_CITY=}")
