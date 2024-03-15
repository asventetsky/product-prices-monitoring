""" Test module """

from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

from src.lambda_exception import LambdaException

with patch.dict(
        "os.environ",
        {
            "REGION": "region",
            "PRODUCTS_TABLE_NAME": "products",
            "PRODUCT_PRICES_TABLE_NAME": "products_prices"
        }
):
    from src.service import fetch_product_price
    from src.service import store_product_price


class TestProductPricesCollectorService(unittest.TestCase):
    """Represents unit tests for service module"""

    @patch("src.service.send_request")
    def test_fetch_product_price_success(self, mock_send_requests):
        """Successful product pricing fetching"""

        mock_send_requests.return_value = {
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

        request = {
            "url": "https://test-url.com/product-id",
            "queryParams": [
                {
                    "name": "id",
                    "pythonExpression": {
                        "exec": "import time",
                        "eval": "str(round(time.time() * 1000)) + \"000001\""
                    }
                }
            ],
            "headers": {
                "Referer": "referer"
            },
            "timeoutSeconds": "5"
        }
        actual_response = fetch_product_price(request)

        expected_response = {
            "id": 20000007085025,
            "name": "Koska Tahin 300 G ( Cam Kavanoz )",
            "price": {
                "regularPrice": 7295,
                "salePrice": 7295,
                "loyaltyPrice": 7295,
                "shownPrice": 7295
            },
            # TODO: introduce current datetime provider
            "date": datetime.now().date().strftime("%Y-%m-%d")
        }

        self.assertEqual(actual_response, expected_response)

    @patch("src.service.send_request")
    def test_fetch_product_price_exception(self, mock_send_requests):
        """Exception on product pricing fetching"""

        mock_send_requests.side_effect = MagicMock(
            side_effect=LambdaException("Error on sending request")
        )

        request = {
            "url": "https://test-url.com/product-id",
            "queryParams": [
                {
                    "name": "id",
                    "pythonExpression": {
                        "exec": "import time",
                        "eval": "str(round(time.time() * 1000)) + \"000001\""
                    }
                }
            ],
            "headers": {
                "Referer": "referer"
            },
            "timeoutSeconds": "5"
        }
        actual_response = fetch_product_price(request)

        self.assertEqual(actual_response, None)

    @patch("src.service.put_product")
    @patch("src.service.put_product_price")
    def test_store_product_price_success(
            self, mock_put_product, mock_put_product_price
    ):
        """Exception on product pricing fetching"""

        mock_put_product.return_value = "OK"
        mock_put_product_price.return_value = "OK"

        product_price = {
            "id": 20000007085025,
            "name": "Koska Tahin 300 G ( Cam Kavanoz )",
            "price": {
                "regularPrice": 7295,
                "salePrice": 7295,
                "loyaltyPrice": 7295,
                "shownPrice": 7295
            },
            "date": datetime.now().date().strftime("%Y-%m-%d")
        }

        actual_response = store_product_price(product_price)

        self.assertEqual(actual_response, None)

    @patch("src.service.put_product")
    def test_store_product_price_exception(self, mock_put_product):
        """Exception on product pricing fetching"""

        mock_put_product.side_effect = MagicMock(
            side_effect=LambdaException("Error occurred while saving product")
        )

        product_price = {
            "id": 20000007085025,
            "name": "Koska Tahin 300 G ( Cam Kavanoz )",
            "price": {
                "regularPrice": 7295,
                "salePrice": 7295,
                "loyaltyPrice": 7295,
                "shownPrice": 7295
            },
            "date": datetime.now().date().strftime("%Y-%m-%d")
        }

        actual_response = store_product_price(product_price)

        self.assertEqual(actual_response, None)


if __name__ == "__main__":
    unittest.main()
