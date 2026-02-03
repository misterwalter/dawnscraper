"""
Scrapes content from ImperialDawn.com so that I can get some scraping practice
"""

import json
from pprint import pprint
import requests
import urllib3


def save_json(json_data, file_name: str) -> None:
    """Saves a json string to file"""
    with open(f"{file_name}.json", "w") as outfile:
        outfile.write(json.dumps(json_data, indent=3, sort_keys=True))


def scrape_tree(tree_id) -> dict:
    """Retrieves an ability tree as a json string"""
    return requests.get(
        f"https://imperialdawn.com/api/data/abilities/search/findInTree?treeId={tree_id}",
        verify=False,
    ).json()


def scrape_categories() -> dict:
    data = requests.get(
        "https://imperialdawn.com/api/data/treeCategories", verify=False
    ).json()
    data = data["_embedded"]["treeCategories"]
    data = [
        {
            "id": tree["id"],
            "name": tree["name"],
            "description": tree["description"],
        }
        for tree in data
    ]
    return data


def main():
    # Turn off the InsecureRequestWarning, broken SSL is part of the motivation for this anyway
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    pprint(scrape_categories())
    save_json(scrape_tree(419), 419)


if __name__ == "__main__":
    main()
