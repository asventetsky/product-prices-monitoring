# pylint: disable=import-error

""" Test module """

import os
import unittest
from unittest.mock import MagicMock, patch
from src.client import send_request


class TestProductPricesCollectorClient(unittest.TestCase):
    """Represents unit tests for client module"""

    @patch("src.client.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5", "PRODUCT_HEADER_REFERER": "header/referer"})
    def test_send_request_success_response(self, mock_requests):
        """Successfully sends request"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": "true",
            "data": {
                "storeProductInfoDTO": {
                    "id": 20000007085025,
                    "name": "Koska Tahin 300 G ( Cam Kavanoz )",
                    "regularPrice": 7295,
                    "salePrice": 7295,
                    "loyaltyPrice": 7295,
                    "shownPrice": 7295
                }
            }
        }

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = send_request()

        expected_response = {
            "successful": "true",
            "data": {
                "storeProductInfoDTO": {
                    "id": 20000007085025,
                    "name": "Koska Tahin 300 G ( Cam Kavanoz )",
                    "regularPrice": 7295,
                    "salePrice": 7295,
                    "loyaltyPrice": 7295,
                    "shownPrice": 7295
                }
            }
        }

        self.assertEqual(actual_response, expected_response)

    @patch("src.client.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "abc", "PRODUCT_HEADER_REFERER": "header/referer"})
    def test_send_request_invalid_timeout_value(self, mock_requests):
        """Invalid value is provided as a timeout"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": "true",
            "data": {
                "storeProductInfoDTO": {
                    "id": 20000007085025,
                    "name": "Koska Tahin 300 G ( Cam Kavanoz )",
                    "regularPrice": 7295,
                    "salePrice": 7295,
                    "loyaltyPrice": 7295,
                    "shownPrice": 7295
                }
            }
        }

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = send_request()

        self.assertEqual(actual_response, None)

    @patch("src.client.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5", "PRODUCT_HEADER_REFERER": "header/referer"})
    def test_send_request_exception(self, mock_requests):
        """Exception occurred during sending the request"""

        mock_requests.get.side_effect = MagicMock(side_effect=Exception("Test exception"))

        actual_response = send_request()

        self.assertEqual(actual_response, None)

    @patch("src.client.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5", "PRODUCT_HEADER_REFERER": "header/referer"})
    def test_send_request_non_200_response_status_code(self, mock_requests):
        """Non-200 response received from external resource"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = send_request()

        self.assertEqual(actual_response, None)

    @patch("src.client.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5", "PRODUCT_HEADER_REFERER": "header/referer"})
    def test_send_request_invalid_response_structure(self, mock_requests):
        """Invalid response structure receive"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = (
            "<product><productPrice>7265</productPrice></product>"
        )

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = send_request()

        self.assertEqual(actual_response, None)


if __name__ == "__main__":
    unittest.main()
