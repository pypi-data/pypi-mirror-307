from typing import Callable

from sincpro_payments_sdk.apps.cybersource.domain import CybersourceCredential

TEST_MERCHANT_ID = "testrest"
TEST_KEY = "08c94330-f618-42a3-b09d-e1e43be5efda"
TEST_SECRET_KEY = "yBJxy6LjM2TmcPGu+GaJrHtkke25fPpUX+UY6/L/1tE="
TEST_PROFILE_ID = None

get_credential: Callable[[], CybersourceCredential | None] = lambda: CybersourceCredential(
    key_id=TEST_KEY,
    secret_key=TEST_SECRET_KEY,
    merchant_id=TEST_MERCHANT_ID,
    profile_id=TEST_PROFILE_ID,
)


class CybersourceCredentialProvider:
    """
    Class to load Cybersource credentials.
    """

    def __init__(self):
        self._get_credential = get_credential

    def get_credential(self) -> CybersourceCredential:
        """Execute the current result of getter function"""
        return self._get_credential()

    def set_cybersource_loader_credentials(
        self, fn: Callable[[], CybersourceCredential]
    ) -> None:
        """Set the getter function to get the Cybersource credentials"""
        self._get_credential = fn


cybersource_credential_provider = CybersourceCredentialProvider()
