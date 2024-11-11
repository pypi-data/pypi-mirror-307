import unittest
from api_exception.exception import APIException
from custom_enum.enums import ExceptionCode, ExceptionStatus
from schemas.response_model import ResponseModel


class TestAPIException(unittest.TestCase):

    def test_api_exception_default(self):
        """Test APIException with default parameters."""
        exception = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED)
        self.assertEqual(exception.error_code, "AUTH-1000")
        self.assertEqual(exception.message, "Incorrect username and password.")
        self.assertEqual(exception.description, "Failed authentication attempt.")
        self.assertEqual(exception.status, ExceptionStatus.FAIL)
        self.assertEqual(exception.http_status_code, 400)

    def test_api_exception_with_custom_message(self):
        """Test APIException with a custom message."""
        custom_message = "Custom error message."
        exception = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED, message=custom_message)
        self.assertEqual(exception.message, custom_message)
        self.assertEqual(exception.description, "Failed authentication attempt.")

    def test_api_exception_with_custom_description(self):
        """Test APIException with a custom description."""
        custom_description = "This is a custom description."
        exception = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED, description=custom_description)
        self.assertEqual(exception.description, custom_description)

    def test_api_exception_with_custom_status_code(self):
        """Test APIException with a custom HTTP status code."""
        custom_status_code = 403
        exception = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED, http_status_code=custom_status_code)
        self.assertEqual(exception.http_status_code, custom_status_code)

    def test_api_exception_to_response(self):
        exception = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED)
        response = exception.to_response()
        expected_response = {
            "error_code": "AUTH-1000",
            "status": "FAIL",
            "message": "Incorrect username and password.",
            "description": "Failed authentication attempt."
        }
        self.assertEqual(response, expected_response)

    def test_response_model_success(self):
        """Test creating a successful ResponseModel instance."""
        response = ResponseModel(data={"key": "value"})
        self.assertEqual(response.status, ExceptionStatus.SUCCESS)
        self.assertEqual(response.message, "Operation completed successfully.")
        self.assertIsNone(response.error_code)
        self.assertIsNone(response.description)
        self.assertEqual(response.data, {"key": "value"})

    def test_response_model_with_custom_message(self):
        """Test ResponseModel with a custom message."""
        response = ResponseModel(data={"key": "value"}, message="Custom success message.")
        self.assertEqual(response.message, "Custom success message.")

    def test_response_model_with_error(self):
        """Test ResponseModel when an error is passed."""
        response = ResponseModel(
            data=None,
            status=ExceptionStatus.FAIL,
            message="An error occurred.",
            error_code="AUTH-1000",
            description="Failed authentication attempt"
        )
        self.assertEqual(response.status, ExceptionStatus.FAIL)
        self.assertEqual(response.message, "An error occurred.")
        self.assertEqual(response.error_code, "AUTH-1000")
        self.assertEqual(response.description, "Failed authentication attempt")
        self.assertIsNone(response.data)


if __name__ == "__main__":
    unittest.main()