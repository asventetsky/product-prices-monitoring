# pylint: disable=import-error

""" Test module """

import unittest
from unittest.mock import patch
from src.main import lambda_handler


class TestPricesCollectorMain(unittest.TestCase):
    """Represent unit tests for main module"""

    @patch("src.main.fetch_product_price")
    def test_lambda_handler_fetch_joke_success(self, mock_fetch_product_price):
        """Unit test for lambda handler function"""

        mock_fetch_product_price.return_value = {
            "regularPrice": 7295,
            "salePrice": 7295,
            "loyaltyPrice": 7295,
            "shownPrice": 7295
        }

        actual_response = lambda_handler({}, {})

        expected_response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": '{"product": {"regularPrice": 7295, "salePrice": 7295, '
            '"loyaltyPrice": 7295, "shownPrice": 7295}}'
        }

        self.assertEqual(actual_response, expected_response)

    @patch("src.main.fetch_product_price")
    def test_lambda_handler_fetch_joke_failure(self, mock_fetch_product_price):
        """Unit test for lambda handler function"""

        mock_fetch_product_price.return_value = None

        actual_response = lambda_handler({}, {})

        expected_response = {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": '{"error": "Internal server error"}',
        }

        self.assertEqual(actual_response, expected_response)


if __name__ == "__main__":
    unittest.main()
