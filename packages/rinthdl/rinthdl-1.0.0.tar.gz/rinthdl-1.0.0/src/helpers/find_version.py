RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"
def find_version(versions, project_version):
    """
    Fetches either the latest or specified version from a list of versions.

    Args:
        versions (list): List of versions.
        project_version (str): Project version.

    Returns:
        dict: Latest or specified version.
    """
    if not versions or type(versions) is str:
        return f"❌ Versions list is empty"

    if project_version:
        for version in versions:
            if version.get("version_number") == project_version:
                return version
        project_id = versions[0].get("project_id")
        return f"❌ No version found matching {project_version} ➜ {BLUE}https://modrinth.com/project/{project_id}{RESET}"
    else:
        return versions[0]
