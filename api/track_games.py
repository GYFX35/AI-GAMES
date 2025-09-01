import requests
import json
import os
from googleapiclient.discovery import build

def get_youtube_api_key():
    """
    Retrieves the YouTube API key from the api_keys.json file.
    """
    # Build the path relative to the current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keys_path = os.path.join(dir_path, "api_keys.json")
    with open(keys_path, "r") as f:
        keys = json.load(f)
        return keys.get("youtube_api_key")

def get_youtube_videos(query, max_results=10):
    """
    Fetches gaming videos from YouTube.
    """
    api_key = get_youtube_api_key()
    if not api_key or api_key == "YOUR_YOUTUBE_API_KEY":
        print("YouTube API key not found or not configured. Skipping YouTube search.")
        return []

    youtube = build("youtube", "v3", developerKey=api_key)

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        videoCategoryId="20",  # Gaming category
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get("items", []):
        videos.append({
            "name": search_result["snippet"]["title"],
            "category": "YouTube Gaming",
            "link": f"https://www.youtube.com/watch?v={search_result['id']['videoId']}",
            "description": search_result["snippet"]["description"],
            "rating": 0,  # YouTube API v3 does not provide ratings in search results
            "player_count": 0  # Not applicable
        })
    return videos

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

def track_games(username, youtube_query="game development"):
    """
    Tracks all game repositories for a given GitHub username and fetches gaming videos from YouTube,
    then saves them to a JSON file.
    """
    try:
        # Get GitHub game repositories
        repos = get_repos(username)
        game_repos = [repo for repo in repos if is_game_repo(repo)]

        games_data = []
        for repo in game_repos:
            games_data.append({
                "name": repo["name"],
                "category": "GitHub Project",
                "link": repo["html_url"],
                "description": repo["description"],
                "rating": repo["stargazers_count"],
                "player_count": repo["forks_count"]
            })

        print(f"Successfully tracked {len(games_data)} game repositories for user {username}.")

        # Get YouTube gaming videos
        youtube_videos = get_youtube_videos(youtube_query)
        games_data.extend(youtube_videos)
        print(f"Successfully fetched {len(youtube_videos)} gaming videos from YouTube.")

        # Save combined data to JSON file
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, "games.json")
        with open(file_path, "w") as f:
            json.dump(games_data, f, indent=4)

        print(f"Successfully saved a total of {len(games_data)} items to games.json.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # It's better to track a more generic user or an organization focused on game development
    track_games("godotengine")
