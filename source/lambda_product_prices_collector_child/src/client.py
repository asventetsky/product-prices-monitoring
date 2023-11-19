import logging
import requests

from src.lambda_exception import LambdaException


def send_request(request):
    try:
        response = _execute_request(request)
        return _parse_json_response(response)
    except LambdaException as error:
        logging.error(error.message)
        return None


def _execute_request(request):
    """Fetch response from remote resource"""

    try:
        headers = construct_headers(request["headers"])
        url = construct_url(request["url"], request["queryParams"])

        return requests.get(
            url,
            headers=headers,
            timeout=request["timeoutSeconds"]
        )
    except Exception as error:
        raise LambdaException(f"Error on sending request: {error}")


def construct_headers(request_headers):
    """Constructs headers"""

    default_headers = {
        'Content-Type': 'text',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'X-PWA': 'true',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'X-FORWARDED-REST': 'true',
        'sec-ch-ua-platform': '"Linux"'
    }
    headers = { **default_headers, **request_headers}

    return headers


def construct_url(request_url, request_query_params):
    """Constructs url with query params"""

    url = request_url

    if request_query_params:
        query_params = []
        for query_param in request_query_params:
            if query_param["pythonExpression"]:
                exec(query_param["pythonExpression"]["exec"])
                query_param_value = eval(query_param["pythonExpression"]["eval"])
            elif query_param["value"]:
                query_param_value = query_param["value"]
            else:
                continue
            query_params.append(f"{query_param['name']}={query_param_value}")
        if query_params:
            url = url + "?" + "&".join(query_params)

    return url


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
