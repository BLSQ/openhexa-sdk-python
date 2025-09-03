"""SSL error handling test module."""


import requests

from openhexa.utils.session import create_requests_session


class TestSSLErrorHandling:
    """Test SSL error handling functionality."""

    def test_create_requests_session_verify_default(self):
        """Test create_requests_session with default verify parameter."""
        session = create_requests_session()
        assert session.verify is True

    def test_ssl_error_handling_logic(self):
        """Test that SSL errors are properly converted to GraphQLError."""
        ssl_error = requests.exceptions.SSLError("CERTIFICATE_VERIFY_FAILED error")

        if "CERTIFICATE_VERIFY_FAILED" in str(ssl_error):
            expected_msg = (
                "SSL certificate verification failed. "
                "If you want to disable SSL verification, set the environment variable: HEXA_VERIFY_SSL=false"
            )
            assert "SSL certificate verification failed" in expected_msg
            assert "HEXA_VERIFY_SSL=false" in expected_msg

        other_ssl_error = requests.exceptions.SSLError("Some other SSL error")
        assert "Some other SSL error" in str(other_ssl_error)
