import argparse
import requests

def main():
    parser = argparse.ArgumentParser('Enter search query')
    parser.add_argument('search_item', type=str, help='The slug of the mod you want')
    args = parser.parse_args()

    API_URL = 'https://api.modrinth.com/v2/'
    search_endpoint = f"search"
    params = {
        "query": args.search_item
    }
    response = requests.get(f"{API_URL}{search_endpoint}", params=params)
    response = response.json()
    hits = response.get("hits")

    title_len = 0
    slug_len = 0
    id_len = 0
    url_len = 0

    for hit in hits:
        if len(hit.get("title")) > title_len:
            title_len = len(hit.get("title"))
        if len(hit.get("slug")) > slug_len:
            slug_len = len(hit.get("slug"))
        if len(hit.get("project_id")) > id_len:
            id_len = len(hit.get("project_id"))
        url = f"https://modrinth.com/project/{hit.get('project_id')}"
        if len(url) > url_len:
            url_len = len(url)

    title_len += 5
    slug_len += 5
    id_len += 5
    url_len += 5

    title = "Title"
    slug = "Slug"
    id_ = "ID"
    url = "URL"
    desc = "Description"

    print(f"{title:<{title_len}}{slug:<{slug_len}}{id_:<{id_len}}{url:<{url_len}}{desc}")
    for hit in hits:
        print(
            f"{hit.get('title'):<{title_len}}"
            f"{hit.get('slug'):<{slug_len}}"
            f"{hit.get('project_id'):<{id_len}}"
            f"https://modrinth.com/project/{hit.get('project_id'):<{url_len - 29}}"
            f"{hit.get('description')}"
        )

    print(f'\nShowing the top {response.get("limit")} results')
