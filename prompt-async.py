import asyncio
import aioredis
import aiohttp
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
RETRIES = 3
BACKOFF_FACTOR = 0.3
MOVIE_DATA_URL = "https://example.com/path/to/valid/movies.json"
OPENAI_MODEL = "gpt-3.5-turbo"
SYSTEM_PROMPT_INITIAL = "You are a helpful assistant and a movie salesman."
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Connect to Redis
redis = None


async def initialize_redis():
    global redis
    redis = await aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT), encoding='utf-8')


async def fetch_movie_data():
    """Fetch the JSON file containing movie data with retries using asyncio and aiohttp."""
    async with aiohttp.ClientSession() as session:
        for attempt in range(RETRIES):
            try:
                async with session.get(MOVIE_DATA_URL) as response:
                    response.raise_for_status()
                    data = await response.json()
                    await redis.set('movies_data', json.dumps(data), expire=3600)  # 1 hour expiration
                    return data
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < RETRIES - 1:
                    await asyncio.sleep(BACKOFF_FACTOR * (2 ** attempt))


async def get_movie_data():
    """Retrieve or fetch movie data with Redis caching."""
    cached_data = await redis.get('movies_data')
    if cached_data:
        return json.loads(cached_data)
    else:
        return await fetch_movie_data()


async def generate_response(prompt):
    """Generate a response using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set. Please set 'OPENAI_API_KEY' in the environment variables.")

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": OPENAI_MODEL,
                "prompt": {"role": "system", "content": SYSTEM_PROMPT_INITIAL} | {"role": "user", "content": prompt},
                "max_tokens": 150
            }
        )
        result = await response.json()
        return result['choices'][0]['message']['content']


async def main():
    await initialize_redis()
    movies_data = await get_movie_data()
    if not movies_data:
        print("Failed to obtain movie data.")
        return

    user_input = input("Please enter your movie preference (e.g., 'Can you suggest some science fiction movies?'): ")
    if "genre" in user_input.lower():
        context, need = "genre", user_input.split("genre")[-1].strip()
    else:
        context, need = "general", user_input

    # Simulate context handling and user profile
    welcome_message = f"Welcome! Looking for {context} movies like '{need}'?"
    response = await generate_response(welcome_message)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
