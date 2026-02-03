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


def scrape_tree_prerequisites(tree_id) -> dict:
    """Mostly a helpful function for scrape_tree but I don't know your life."""
    data = requests.get(
        f"https://imperialdawn.com/api/data/abilityTrees/prerequisiteGraph?treeId={tree_id}",
        verify=False,
    ).json()
    return {ability["id"]: ability["prereqs"] for ability in data}


def scrape_tree(tree_id) -> dict:
    """Retrieves an ability tree with all abilities as a json string"""
    prereqs = scrape_tree_prerequisites(tree_id)

    data = requests.get(
        f"https://imperialdawn.com/api/data/abilities/search/findInTree?treeId={tree_id}",
        verify=False,
    ).json()
    data = data["_embedded"]["abilities"]
    data = [
        {
            "id": ability["id"],
            "name": ability["name"],
            "description": ability["description"],
            "type": ability["type"],
            "checkTrait": ability["checkTrait"],
            "saveTrait": ability["saveTrait"],
            "prereqs": prereqs[ability["id"]],
        }
        for ability in data
    ]
    return data


def scrape_trees_in_category(category_id) -> dict:
    data = requests.get(
        f"https://imperialdawn.com/api/data/treeCategories/{category_id}/trees",
        verify=False,
    ).json()
    data = data["_embedded"]["abilityTrees"]
    data = [
        {
            "id": tree["id"],
            "name": tree["name"],
            "description": tree["description"],
            "learnable": tree["learnable"],
        }
        for tree in data
    ]
    return data


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

    # Pull Categories
    categories = scrape_categories()
    save_json(categories, "categories")

    # Pull Trees
    all_trees = []
    for category in categories:
        print(f"Pulling {category['name']}")
        trees = scrape_trees_in_category(category["id"])
        all_trees.extend(trees)
        pprint(trees)
        for tree in trees:
            save_json(scrape_tree(tree["id"]), tree["name"].replace("/", ""))

    save_json(all_trees, "trees")


if __name__ == "__main__":
    main()
