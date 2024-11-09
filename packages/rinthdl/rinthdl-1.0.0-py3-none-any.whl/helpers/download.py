import os

import requests

def download_file(url, filename, path):
    """
    Download a file from url and save it to path.

    Args:
        url (str): URL to download.
        filename (str): Filename to save the downloaded file.
        path (str): Path to save the downloaded file.

    Returns:
        str: Only Errors are returned. File is being downloaded if no error occurrs.
    """
    if not path:
        print("❌ Path is empty")
        exit(1)

    path = os.path.expanduser(path)

    if not os.path.exists(path):
        os.makedirs(path)

    try:
        download = requests.get(url)
    except requests.exceptions.ConnectionError:
        return f"❌ Connection error during file download"
    except requests.exceptions.Timeout:
        return f"❌ Connection time out during file download"
    except requests.exceptions.HTTPError:
        return f"❌ HTTP error during file download."

    try:
        with open(f"{path}/{filename}", 'wb') as f:
            f.write(download.content)
            return f"✔️ Downloaded {filename} to {path}{filename}"
    except IOError:
        return f"❌ IO error during file download"
    except Exception as e:
        return f"❌ Error writing file: {filename} due to exception: {e}"

def find_url(version):
    """
    Finds the URL and filename of a given version dict.

    Args:
        version (dict): Dictionary of version info.

    Returns:
        str: URL and filename.
    """
    if not version:
        return f"❌ The provided version is empty."

    if 'files' not in version:
        return f"❌ The provided version does not contain any files."

    url_list = version.get("files")

    if not type(url_list) == list:
        return f"❌ The files attribute is not a list."

    if not url_list:
        return f"❌ The files list is empty."

    first_file = url_list[0]

    if not type(first_file) == dict:
        return f"❌ The file entry is not a valid dictionary."

    url = first_file.get("url")
    filename = first_file.get("filename")

    if not url or not filename:
        return f"❌ The file entry does not contain url and filename."

    return url, filename

def validate_path(path):
    path = os.path.expanduser(path)

    if not os.path.exists(path):
        if input(f"Should I create path {path}? (y|N): ").lower() in ["y", "yes"]:
            os.makedirs(path)
        else:
            print(f"❌ Path {path} wasn't allowed to be created.")
            exit(1)
