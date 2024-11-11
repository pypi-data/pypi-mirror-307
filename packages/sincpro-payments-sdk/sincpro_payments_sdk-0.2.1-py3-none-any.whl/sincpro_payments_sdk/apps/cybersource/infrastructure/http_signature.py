import base64
import hashlib
import hmac
from datetime import datetime, timezone

from requests.auth import AuthBase

from sincpro_payments_sdk.apps.cybersource.domain.credentials import CybersourceCredential


def generate_hash(body: str) -> str:
    """Generate a Base64-encoded SHA-256 digest for the request body."""
    _body_bytes = body
    if isinstance(body, str):
        _body_bytes = body.encode("utf-8")
    digest = hashlib.sha256(_body_bytes).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_str_signature(secret_key: bytes, string_to_sign: str) -> str:
    """Build the signature for the HTTP request."""
    signature = base64.b64encode(
        hmac.new(
            secret_key,
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    ).decode("utf-8")
    return signature


class CyberSourceAuth(AuthBase):
    """Custom authentication for CyberSource API requests."""

    def __init__(
        self,
        cybersource_credentials: CybersourceCredential,
    ):
        """
        Initialize with required CyberSource credentials.

        :param key_id: The key ID provided by CyberSource.
        :param secret_key: The secret key provided by CyberSource (base64-encoded).
        :param merchant_id: Your merchant ID.
        """
        self.key_id = cybersource_credentials.key_id
        self.secret_key = base64.b64decode(
            cybersource_credentials.secret_key
        )  # Decode base64 secret key
        self.merchant_id = cybersource_credentials.merchant_id
        self.profile_id = cybersource_credentials.profile_id

    def generate_signature_for_get_method(
        self,
        method: str,
        resource: str,
        date: str,
        host: str,
    ):
        """Generate the HTTP GET Signature for CyberSource authentication."""
        string_to_sign = (
            f"host: {host}\n"
            f"v-c-date: {date}\n"
            f"(request-target): {method.lower()} {resource}\n"
            f"v-c-merchant-id: {self.merchant_id}"
        )

        signature_header = (
            f'keyid="{self.key_id}", '
            f'algorithm="HmacSHA256", '
            f'headers="host v-c-date (request-target) v-c-merchant-id", '
            f'signature="{build_str_signature(self.secret_key, string_to_sign)}"'
        )

        return signature_header

    def generate_signature_with_body(
        self, method: str, resource: str, date: str, digest: str, host: str
    ) -> str:
        """Generate the HTTP Signature for CyberSource authentication."""

        string_to_sign = (
            f"host: {host}\n"
            f"v-c-date: {date}\n"
            f"(request-target): {method.lower()} {resource}\n"
            f"digest: SHA-256={digest}\n"
            f"v-c-merchant-id: {self.merchant_id}"
        )

        signature_header = (
            f'keyid="{self.key_id}", '
            f'algorithm="HmacSHA256", '
            f'headers="host v-c-date (request-target) digest v-c-merchant-id", '
            f'signature="{build_str_signature(self.secret_key, string_to_sign)}"'
        )

        return signature_header

    def build_headers(self, method: str, resource: str, body: str, host: str) -> dict:
        """Build the required headers for CyberSource request authentication."""
        datetime_required_format = datetime.now(timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        headers = {
            "Content-Type": "application/json",
            "host": host,
            "v-c-merchant-id": self.merchant_id,
            "v-c-date": datetime_required_format,
        }

        if self.profile_id:
            headers["profile-id"] = self.profile_id

        match method.upper():
            case "GET":
                signature = self.generate_signature_for_get_method(
                    method, resource, datetime_required_format, host
                )
                headers["signature"] = signature
            case _:
                body_hash = generate_hash(body)
                signature = self.generate_signature_with_body(
                    method, resource, datetime_required_format, body_hash, host
                )
                headers["digest"] = f"SHA-256={body_hash}"
                headers["signature"] = signature

        return headers

    def __call__(self, request):
        """Customize the request with headers for CyberSource authentication."""
        body = request.body
        host = request.url.split("//")[-1].split("/")[0]
        resource = request.path_url

        headers = self.build_headers(request.method, resource, body, host)
        request.headers.update(headers)

        return request
