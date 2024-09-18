import openai
import os


def generate_response(prompt):
    # Check if the API key is retrieved correctly; raise an error if not
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set. Please set 'OPENAI_API_KEY' in the environment variables.")

    # Initialize the client with the retrieved API key
    client = openai.OpenAI(api_key=api_key)

    # Create a chat completion with the prompt
    chat_completion = client.chat.completions.create(
        model="dall-e-3",
        messages=[
            # Replacing the fixed statement with prompt variable
            {"role": "user", "content": prompt}
        ]
    )

    # Extracting the response message from the AI
    response_message = chat_completion["choices"][0]["message"]["content"]

    return response_message


# Example usage of the function
prompt = "Explain the significance of AI in modern technology."
response = generate_response(prompt)
print(response)