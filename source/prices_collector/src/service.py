""" Service for sending request to external resource """

import logging
import os

import requests

from datetime import date
from src.service_exception import ServiceError

logging.getLogger().setLevel(logging.INFO)


def fetch_product_price():
    """Fetch and extract joke from remote resource"""
    try:
        config = _fetch_config()
        response = _execute_request(config)
        return _extract_product_price(response)
    except ServiceError as error:
        logging.error(error.message)
        return None


def _fetch_config():
    """Fetch config"""
    config = {}
    try:
        config["URL"] = os.environ["PRODUCTS_URL"]
        config["TIMEOUT"] = int(os.environ["PRODUCTS_TIMEOUT"])
        return config
    except Exception as error:
        raise ServiceError(f"Error occurred while fetching environment variables: {error}")


def _execute_request(config):
    """Fetch response from remote resource"""
    try:
        headers = {
            'Content-Type': 'text',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'X-PWA': 'true',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.migros.com.tr/koska-tahin-300-g-cam-kavanoz-p-6c1be1',
            'X-FORWARDED-REST': 'true',
            'sec-ch-ua-platform': '"Linux"'
        }
        response = requests.get(
            config["URL"],
            headers=headers,
            timeout=config["TIMEOUT"],
        )
    except Exception as error:
        raise ServiceError(f"Error on sending request: {error}")

    _handle_response(response)

    return response


def _handle_response(response):
    """Handle response from remote resource"""
    if response.status_code != 200:
        raise ServiceError(f"Non 200 status received: {response.status_code}")


def _extract_product_price(response):
    """Extract product price from the response"""
    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise ServiceError(f"Error on extracting the product price: {error}")

    if not isinstance(json_response, dict):
        raise ServiceError(f"Invalid response structure. Original response: `{json_response}`")

    try:
        product_price = {
            "id": int(json_response["data"]["storeProductInfoDTO"]["id"]),
            "name": json_response["data"]["storeProductInfoDTO"]["name"],
            "regularPrice": json_response["data"]["storeProductInfoDTO"]["regularPrice"],
            "salePrice": json_response["data"]["storeProductInfoDTO"]["salePrice"],
            "loyaltyPrice": json_response["data"]["storeProductInfoDTO"]["loyaltyPrice"],
            "shownPrice": json_response["data"]["storeProductInfoDTO"]["shownPrice"],
            "date": date.today()
        }
        return product_price
    except Exception:
        raise ServiceError(f"Error on extracting the product price. Original response: `{json_response}`")
