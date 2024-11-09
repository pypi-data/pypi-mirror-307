from helpers.fetch_project_id_from_slug import check_project
from helpers.find_dependencies import find_dependencies
from helpers.find_project_meta import find_project_meta
from helpers.download import find_url, download_file, validate_path
from helpers.fetch_versions import fetch_versions
from helpers.find_version import find_version

import argparse
import json
import os
import shutil

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

def get_url(version):
    """
    Wrapper for find_url() with type checking and error handling.

    Args:
         version (dict): Version dictionary to be checked for URL.

    Returns:
        str: url and filename
    """
    spam = find_url(version)
    if not type(spam) == tuple:
        return spam
    version_url, version_filename = spam
    return version_url, version_filename

def fetch_id(slug):
    """
    Wrapper of  check_project() with error handling.

    Args:
        slug (str): Slug of the project.

    Returns:
        str: project id
    """
    project_id = check_project(slug)
    if project_id.startswith("❌"):
        print(f"{project_id}")
    return project_id

def find_duplicates(projects):
    """
     Find duplicate project declarations in the modpack.json

     Args:
         projects (list): List of project declarations from the modpack.json

    Returns:
        Nothing, only prints Message during its runtime if duplicates are found.
    """
    names = [project['name'] for project in projects]
    seen = set()
    duplicates = []

    for name in names:
        if name in seen:
            duplicates.append(name)
        else:
            seen.add(name)
    if duplicates:
        print(f"{BLUE}Duplicates found:{RESET}")
    for duplicate in duplicates:
        print(f"    - {duplicate}")

def main():
    parser = argparse.ArgumentParser('Specify the path of your modpack config.json')
    parser.add_argument('modpack_file', type=str, help='Path of your modpack.json')

    modpack_file = parser.parse_args().modpack_file
    try:
        with open(modpack_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"❌ Your modpack file couldn't be found at {modpack_file} ")
        exit(1)
    except json.decoder.JSONDecodeError:
        print(f"❌ Your modpack file couldn't be decoded at {modpack_file} ")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    find_duplicates(data["projects"])

    modpack = data["name"]
    game_version = data["game_version"]
    path = data["path"]
    download_dependencies = data["deps"]

    print(f"{BLUE}Downloading assets for {modpack}{RESET}")

    # Remove old files from download dir
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.makedirs(path)

    for project in data["projects"]:
        download_path = path
        validate_path(path)

        name_type_map = {
            "mod": "mods",
            "resourcepack": "resourcepacks",
            "modpack": "modpacks",
            "datapack": "datapacks",
            "shader": "shaderpacks",
            "plugin": "plugins"
        }
        project_type = project["type"]
        project_platform = project["platform"]
        project_version = project["version"]

        download_path = os.path.join(download_path, name_type_map.get(project_type, project_type))

        project_id = fetch_id(project["name"])
        if project_id.startswith("❌"):
            continue

        versions = fetch_versions(project_id, game_version, project_platform)
        if type(versions) == str:
            print(f"{versions}")
            continue

        version = find_version(versions, project_version)
        if type(version) == str:
            print(f"{version}")
            continue

        url, version_filename = get_url(version)
        try:
            download_file(url, version_filename, str(download_path))
            print(f"✔️ Successfully downloaded {project['name']}.")
        except Exception as e:
            print(f"{RED}❌ An unexpected error occurred during the download of {project['name']}: {e}{RESET}")

        if not download_dependencies.capitalize() == "True":
            continue

        dependencies = find_dependencies(version)
        for dependency in dependencies:
            template = {"name": "", "version": "", "platform": "", "type": ""}

            slug = find_project_meta(dependency)[2]
            possible_project_loader = find_project_meta(dependency)[1][0]
            project_type = find_project_meta(dependency)[0]
            if not slug or slug.startswith("❌"):
                print(f"Error in finding dependency of {dependency}: {slug}")
                continue

            slug_exists_in_modpack_json = any(project['name'] == slug for project in data["projects"])

            if slug_exists_in_modpack_json:
                continue

            project_id = fetch_id(dependency)
            if project_id.startswith("❌"):
                continue
            template["name"] = slug
            template["type"] = project_type
            template["platform"] = possible_project_loader

            print(f""
                    f'ℹ️ {project["name"].capitalize()} has a possible '
                    f'dependency for {BLUE}https://modrinth.com/project/{slug}{RESET}\n'
                    f'ℹ️ Template for your modpack.json: {json.dumps(template)}'
                  )


if __name__ == "__main__":
    main()
