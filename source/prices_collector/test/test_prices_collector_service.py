# pylint: disable=import-error

""" Test module """

import os
import unittest
from unittest.mock import MagicMock, patch
from src.service import fetch_product_price


class TestPricesCollectorService(unittest.TestCase):
    """Represents unit tests for service module"""

    @patch("src.service.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5"})
    def test_fetch_product_price_success_response(self, mock_requests):
        """Successful product pricing fetching"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": "true",
            "data": {
                "storeProductInfoDTO": {
                    "regularPrice": 7295,
                    "salePrice": 7295,
                    "loyaltyPrice": 7295,
                    "shownPrice": 7295
                }
            }
        }

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = fetch_product_price()

        expected_response = {
            "regularPrice": 7295,
            "salePrice": 7295,
            "loyaltyPrice": 7295,
            "shownPrice": 7295
        }

        self.assertEqual(actual_response, expected_response)

    @patch("src.service.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "abc"})
    def test_fetch_product_price_invalid_timeout_value(self, mock_requests):
        """Invalid value is provided as a timeout"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": "true",
            "data": {
                "storeProductInfoDTO": {
                    "regularPrice": 7295,
                    "salePrice": 7295,
                    "loyaltyPrice": 7295,
                    "shownPrice": 7295
                }
            }
        }

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = fetch_product_price()

        self.assertEqual(actual_response, None)

    @patch("src.service.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5"})
    def test_fetch_product_price_exception_fetching_joke(self, mock_requests):
        """Exception occurred during sending the request"""

        mock_requests.get.side_effect = MagicMock(side_effect=Exception("Test exception"))

        actual_response = fetch_product_price()

        self.assertEqual(actual_response, None)

    @patch("src.service.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5"})
    def test_fetch_product_price_non_200_response_status_code(self, mock_requests):
        """Non-200 response received from external resource"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = fetch_product_price()

        self.assertEqual(actual_response, None)

    @patch("src.service.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5"})
    def test_fetch_product_price_invalid_response_structure(self, mock_requests):
        """Invalid response structure receive"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = (
            "<product><productPrice>7265</productPrice></product>"
        )

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = fetch_product_price()

        self.assertEqual(actual_response, None)

    @patch("src.service.requests")
    @patch.dict(os.environ, {"PRODUCTS_URL": "https://url", "PRODUCTS_TIMEOUT": "5"})
    def test_fetch_product_price_invalid_json_response(self, mock_requests):
        """Missing prices in a response"""

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": "true",
            "data": {
                "storeProduct": {
                    "regularPrice": 7295,
                    "salePrice": 7295,
                    "loyaltyPrice": 7295,
                    "shownPrice": 7295
                }
            }
        }

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response

        actual_response = fetch_product_price()

        self.assertEqual(actual_response, None)


if __name__ == "__main__":
    unittest.main()
