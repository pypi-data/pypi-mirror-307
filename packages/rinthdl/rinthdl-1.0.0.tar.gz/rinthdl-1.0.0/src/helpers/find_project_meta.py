import json

import requests

API_URL = 'https://api.modrinth.com/v2/'

def find_project_meta(project_id):
    """
    Find project meta data.

    Args:
        project_id (string): Project ID.

    Returns:
        tuple: project_type [str], project_loaders [list], project_slug [str]
    """
    endpoint = f"project/{project_id}"
    response = ""
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return f"❌ HTTP error occurred {response.status_code}."
    except requests.exceptions.RequestException as err:
        return f"❌ Network error occurred: {err}"

    try:
        data = response.json()
    except json.JSONDecodeError as jde:
        return f"❌ Response is not valid JSON:\n{jde.doc}\n{jde.pos}"

    if not data:
        return f"❌ No versions found matching ➜ https://modrinth.com/project/{project_id} "

    try:
        project_type = data.get("project_type")
        project_loaders = data.get("loaders")
        project_slug = data.get("slug")
    except KeyError:
        return f"❌ The Project seems not to have a type."

    if not type:
        return f"❌ The Project seems not to have a type."

    return project_type, project_loaders, project_slug
