"""SSL error handling test module."""


import pytest
import requests

from openhexa.sdk.utils import SSLError, handle_ssl_error
from openhexa.utils.session import create_requests_session


class TestSSLErrorHandling:
    """Test SSL error handling functionality."""

    def test_create_requests_session_verify_default(self):
        """Test create_requests_session with default verify parameter."""
        session = create_requests_session()
        assert session.verify is True

    def test_ssl_error_handling_raises_custom_exception(self):
        ssl_error = requests.exceptions.SSLError("CERTIFICATE_VERIFY_FAILED error")

        with pytest.raises(SSLError) as exc_info:
            handle_ssl_error(ssl_error)

        error_msg = str(exc_info.value)
        assert "SSL certificate verification failed" in error_msg
        assert "HEXA_VERIFY_SSL=false" in error_msg

    def test_non_ssl_error_passes_through(self):
        non_ssl_error = requests.exceptions.RequestException("Not an SSL error")
        handle_ssl_error(non_ssl_error)
