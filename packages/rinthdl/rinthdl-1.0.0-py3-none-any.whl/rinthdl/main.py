from helpers.fetch_project_id_from_slug import check_project as fetch_id
from helpers.fetch_versions import fetch_versions
from helpers.find_version import find_version
from helpers.find_dependencies import find_dependencies
from helpers.find_project_meta import find_project_meta
from helpers.download import find_url, download_file, validate_path

import argparse
import json

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"


def get_id(slug):
    """
    Wrapper for fetch_id with minor error handling

    Args:
        slug (str): slug of project

    Returns:
        str: Project ID
    """
    project_id = fetch_id(slug)

    if not project_id:
        project_id = "❌ Error Project ID is empty"

    return f"{project_id}"

def get_file(version, path):
    egg = find_url(version)
    if not type(egg) == tuple:
        print(f"{RED}{egg}{RESET}")
        exit(1)
    url, filename = egg

    if not path:
        print("❌ Path is empty")
        exit(1)

    path = path

    if download_file(url, filename, path):
        print(f"✔️ Successfully downloaded: {filename}.")
    else:
        print(f"❌ An Error occurred during the download of {filename}")


def main():
    parser = argparse.ArgumentParser(description='Fetch all versions of a project.')
    parser.add_argument('operation', help='What do you want to do?')
    parser.add_argument('slug', help='The project slug.')
    parser.add_argument('--game_version', help='The game version.')
    parser.add_argument('--platform', help='The platform.')
    parser.add_argument('--project_version', help='The project version.')
    parser.add_argument('--path', help='The path to download to.')

    args = parser.parse_args()
    game_version = args.game_version
    platform = args.platform
    project_version = args.project_version
    path = args.path

    project_id = get_id(args.slug)
    versions = fetch_versions(project_id, game_version, platform)
    version = find_version(versions, project_version)
    dependencies = find_dependencies(version)
    meta = find_project_meta(project_id)

    if project_id.startswith("❌"):
        print(project_id)
        exit(1)
    elif type(versions) != list:
        print(versions)
        exit(1)
    elif type(version) != dict:
        print(version)
        exit(1)
    elif type(meta) != tuple:
        print(meta)
        exit(1)

    if args.operation == "get_id":
        print(project_id)
        exit(0)
    elif args.operation == "get_versions":
        if type(versions) == list:
            print(json.dumps(versions, indent=4))
        else:
            print(versions)
        exit(0)
    elif args.operation == "get_version":
        print(json.dumps(version, indent=4))
        exit(0)
    elif args.operation == "get_dependencies":
        if not dependencies:
            print("✔️ No dependencies found")
            exit(0)
        print(dependencies)
        exit(0)
    elif args.operation == "get_project_meta":
        print(f"Type: {meta[0].capitalize()}")
        print("Loaders:", end=" ")
        for loader in meta[1]:
            print(f"{loader.capitalize()}", end=" ")
        print(f"\nSlug: {meta[2]}")
        exit(0)
    elif args.operation == "download":
        validate_path(path)
        get_file(version, path)

if __name__ == '__main__':
    main()


