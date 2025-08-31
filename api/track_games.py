import requests
import json
import os

def get_repos(username):
    """
    Fetches all public repositories for a given GitHub username.
    """
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def is_game_repo(repo):
    """
    Determines if a repository is a game repository based on its name, description, or topics.
    """
    game_keywords = ["game", "games", "gaming", "gamedev"]
    repo_name = repo.get("name", "").lower()
    description = repo.get("description", "").lower() if repo.get("description") else ""
    topics = repo.get("topics", [])

    if any(keyword in repo_name for keyword in game_keywords):
        return True
    if any(keyword in description for keyword in game_keywords):
        return True
    if any(keyword in topic for topic in topics for keyword in game_keywords):
        return True

    return False

def track_games(username):
    """
    Tracks all game repositories for a given GitHub username and saves them to a JSON file.
    """
    try:
        repos = get_repos(username)
        game_repos = [repo for repo in repos if is_game_repo(repo)]

        games_data = []
        for repo in game_repos:
            games_data.append({
                "name": repo["name"],
                "category": "GitHub Games",
                "link": repo["html_url"],
                "description": repo["description"],
                "rating": repo["stargazers_count"],
                "player_count": repo["forks_count"]
            })

        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, "games.json")
        with open(file_path, "w") as f:
            json.dump(games_data, f, indent=4)

        print(f"Successfully tracked {len(games_data)} game repositories for user {username}.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    track_games("gyfx35")
