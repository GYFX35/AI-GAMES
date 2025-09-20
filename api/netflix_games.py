import requests
from bs4 import BeautifulSoup
import json
import os

def get_netflix_games():
    """
    Scrapes the IPVanish website to get a list of Netflix games and their descriptions.
    """
    URL = "https://www.ipvanish.com/blog/best-games-on-netflix/"
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    games = []

    # The game titles are in h3 tags, and the descriptions are in the following p tags.
    for h3 in soup.find_all('h3'):
        title = h3.get_text(strip=True)
        # Stop if we reach the "How Netflix Games works" section
        if "How Netflix Games works" in title:
            break

        # Find the next p tag which should be the description
        description_tag = h3.find_next_sibling('p')
        if description_tag:
            description = description_tag.get_text(strip=True)
            games.append({'title': title, 'description': description})

    return games

def save_games_to_json():
    """
    Saves the scraped games to a JSON file.
    """
    games = get_netflix_games()
    if games:
        # Build the path relative to the current file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, '..', 'frontend', 'data', 'netflix_games.json')

        with open(file_path, 'w') as f:
            json.dump(games, f, indent=4)
        print(f"Successfully saved {len(games)} games to {file_path}")
    else:
        print("No games found or error in scraping.")

if __name__ == '__main__':
    save_games_to_json()
