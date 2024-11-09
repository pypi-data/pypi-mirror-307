import json

import requests

API_URL = 'https://api.modrinth.com/v2/'

def fetch_versions(project_id, game_version, platform):
    """
    Fetches all versions of a modrinth project.

    Args:
        project_id (str): The project ID.
        game_version (str): The game version.
        platform (str): The platform.

    Returns:
        list: All versions of the project.
    """
    if not project_id:
        return  "❌ A project ID is required."
    if not game_version:
        return "❌ A game version is required."
    if not platform:
        return "❌ A platform is required."

    endpoint = f"project/{project_id}/version"
    params = {
        "game_versions" : f'["{game_version}"]',
        "loaders"       : f'["{platform}"]',
    }
    response = ""

    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
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
        return f"❌ No versions found matching {game_version}, {platform} ➜ https://modrinth.com/project/{project_id} "

    return data
