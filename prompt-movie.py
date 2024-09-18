import requests
import openai
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
RETRIES = 3
BACKOFF_FACTOR = 0.3
MOVIE_DATA_URL = "https://example.com/path/to/valid/movies.json"  # Update this URL to a valid one
OPENAI_MODEL = "gpt-3.5-turbo"
SYSTEM_PROMPT = "You are a helpful assistant and a movie salesman."

# Cache to store search results
cache = {}

def _fetch_movie_data(url, retries=RETRIES, backoff_factor=BACKOFF_FACTOR):
    """Fetch the JSON file containing movie data with retries."""
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))
            else:
                logging.error("All attempts to fetch movie data have failed.")
                return None

def _search_movies(movies_data, key, value):
    """Search for movies by a specific key and value."""
    cache_key = f"{key}:{value.lower()}"
    if cache_key in cache:
        return cache[cache_key]

    results = [movie for movie in movies_data if key in movie and value.lower() in movie[key].lower()]
    cache[cache_key] = results
    return results

def _determine_context(user_input):
    """Determine the context and user needs from the input."""
    if "genre" in user_input.lower():
        return "genre", user_input.split("genre")[-1].strip()
    elif "actor" in user_input.lower():
        return "actor", user_input.split("actor")[-1].strip()
    else:
        return "general", user_input

def _recommend_movies(movies_data, context, need):
    """Recommend movies based on context and user needs."""
    if context == "genre":
        return _search_movies(movies_data, "genre", need)
    elif context == "actor":
        return _search_movies(movies_data, "actors", need)
    else:
        return []

def _generate_response(prompt):
    """Generate a response using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set. Please set 'OPENAI_API_KEY' in the environment variables.")

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return None

def main():
    """Main function to run the movie recommendation system."""
    movies_data = _fetch_movie_data(MOVIE_DATA_URL)
    if not movies_data:
        return

    user_input = input("Please enter your movie preference (e.g., 'Can you suggest some science fiction movies?'): ")
    context, need = _determine_context(user_input)
    recommended_movies = _recommend_movies(movies_data, context, need)

    if recommended_movies:
        movie_titles = [movie['title'] for movie in recommended_movies]
        prompt = f"I have found the following {context} movies: {', '.join(movie_titles)}. Can you help me choose one?"
    else:
        prompt = f"No {context} movies found. Can you suggest some other genres?"

    response = _generate_response(prompt)
    if response:
        print(response)
    else:
        print("No response generated.")

if __name__ == "__main__":
    main()