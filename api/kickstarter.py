import json
import os

def get_projects(query: str):
    """
    Returns a list of mock Kickstarter projects.
    This is a mock implementation because Kickstarter blocks scraping.
    """
    # Load mock data from a JSON file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, "..", "data", "kickstarter_projects.json")

    try:
        with open(data_path, "r") as f:
            projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a default list if the file doesn't exist or is empty
        projects = [
            {
                "title": "Awesome Game Project",
                "blurb": "A revolutionary new game that will change everything.",
                "link": "https://www.kickstarter.com/projects/user/awesome-game-project"
            },
            {
                "title": "Indie RPG Adventure",
                "blurb": "Explore a vast world in this epic role-playing game.",
                "link": "https://www.kickstarter.com/projects/user/indie-rpg-adventure"
            }
        ]

    # Filter projects based on the query
    if not query:
        return projects

    query = query.lower()
    return [
        project for project in projects
        if query in project["title"].lower() or query in project["blurb"].lower()
    ]
