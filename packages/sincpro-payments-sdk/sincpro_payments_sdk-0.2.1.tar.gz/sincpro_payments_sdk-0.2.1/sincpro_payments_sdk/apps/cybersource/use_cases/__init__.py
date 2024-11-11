from sincpro_framework import ApplicationService as _ApplicationService
from sincpro_framework import DataTransferObject
from sincpro_framework import Feature as _Feature
from sincpro_framework import UseFramework as _UseFramework

from sincpro_payments_sdk.apps.cybersource.adapters.cybersource_rest_api import (
    payer_auth_adapter,
    payment_adapter,
    tokenization_adapter,
)


class DependencyContextType:
    token_adapter: tokenization_adapter.TokenizationAdapter
    payment_adapter: payment_adapter.PaymentAdapter
    payer_auth_adapter: payer_auth_adapter.PayerAuthenticationAdapter


cybersource = _UseFramework()
cybersource.add_dependency("token_adapter", tokenization_adapter.TokenizationAdapter())
cybersource.add_dependency("payment_adapter", payment_adapter.PaymentAdapter())
cybersource.add_dependency(
    "payer_auth_adapter", payer_auth_adapter.PayerAuthenticationAdapter()
)


class Feature(_Feature, DependencyContextType):
    pass


class ApplicationService(_ApplicationService, DependencyContextType):
    pass


# Add use cases (Application Services and Features)
from . import payments, tokenization

__all__ = [
    "cybersource",
    "tokenization",
    "payments",
    "Feature",
    "ApplicationService",
    "DataTransferObject",
]
