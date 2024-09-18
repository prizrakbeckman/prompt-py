# Movie Recommendation System

## Overview

This project is a movie recommendation system that fetches movie data from a JSON file, searches for movies based on user criteria, and uses OpenAI's GPT-3.5-turbo model to guide the user in choosing a movie. The system also caches search results and collects user feedback to improve future recommendations.

## Functional Details

### Features

1. **Fetch Movie Data**: Retrieves movie data from a JSON file hosted on GitHub.
2. **Search Movies**: Allows users to search for movies based on specific criteria (e.g., genre).
3. **Generate Recommendations**: Uses OpenAI's GPT-3.5-turbo model to provide movie recommendations and guide the user in choosing a movie.
4. **Cache Results**: Caches search results to improve performance and avoid redundant searches.
5. **User Feedback**: Collects user feedback to improve future recommendations.

### Usage

1. **Search for Movies**: The user can search for movies by specifying a genre or other criteria.
2. **Get Recommendations**: The system uses the LLM to provide recommendations and guide the user.
3. **Provide Feedback**: The user can provide feedback on the recommended movies to help improve future recommendations.

## Technical Details

### Dependencies

- `requests`: For fetching the JSON file from GitHub.
- `openai`: For interacting with OpenAI's GPT-3.5-turbo model.
- `json`: For parsing JSON data.
- `os`: For accessing environment variables.

### Environment Setup

1. **Install Dependencies**:
   ```bash
   pip install requests openai