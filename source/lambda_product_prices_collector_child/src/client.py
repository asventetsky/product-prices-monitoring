import os

import logging
import requests
import time

from src.lambda_exception import LambdaException


def send_request(path, referer):
    try:
        config = _fetch_config()
        response = _execute_request(config, path, referer)
        return _parse_json_response(response)
    except LambdaException as error:
        logging.error(error.message)
        return None


def _fetch_config():
    """Fetch config"""
    config = {}
    try:
        config["URL"] = os.environ["PRODUCTS_URL"]
        config["URL_PROVIDE_TIMESTAMP"] = bool(os.environ["PRODUCTS_URL_PROVIDE_TIMESTAMP"])
        config["TIMEOUT"] = int(os.environ["PRODUCTS_TIMEOUT"])
        return config
    except Exception as error:
        raise LambdaException(f"Error on fetching environment variables: {error}")


def _execute_request(config, path, referer):
    """Fetch response from remote resource"""

    try:
        headers = {
            'Content-Type': 'text',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'X-PWA': 'true',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': referer,
            'X-FORWARDED-REST': 'true',
            'sec-ch-ua-platform': '"Linux"'
        }
        url = config["URL"] + path
        if config["URL_PROVIDE_TIMESTAMP"]:
            query_params = f"?reid={round(time.time() * 1000)}000001"
            url = url + query_params
        return requests.get(
            url,
            headers=headers,
            timeout=config["TIMEOUT"]
        )
    except Exception as error:
        raise LambdaException(f"Error on sending request: {error}")


def _parse_json_response(response):
    """Handle response from remote resource"""

    if response.status_code != 200:
        raise LambdaException(f"Non 200 status received: {response.status_code}. Url: {response.request.url}, headers: {response.request.headers}")

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise LambdaException(f"Invalid response structure. Original response: `{response}`. Error: {error}")

    if not isinstance(json_response, dict):
        raise LambdaException(f"Invalid response structure. Original response: `{json_response}`")

    return json_response
