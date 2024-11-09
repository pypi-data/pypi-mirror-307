import json

import requests

API_URL = 'https://api.modrinth.com/v2/'

def check_project(slug):
    """
    Checks the Modrinth API for a project with the given slug.

    Args:
        slug (str): The slug of the project to check.

    Returns:
        str: The project ID if found, or an error message.
    """

    check_endpoint = f"project/{slug}/check"

    try:
        response = requests.get(f"{API_URL}{check_endpoint}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"❌ Network error occurred: {err}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        return "❌ Response is not valid JSON"

    if len(data) != 1:
        return "❌ Unexpected number of items in response"

    value = next(iter(data.values()))
    if not value:
        return "❌ Project ID is empty"
    if not value.isalnum():
        return "❌ The project ID contains invalid characters; expected alphanumeric."

    return value
