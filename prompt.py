import openai
import os

api_key = os.getenv('OPENAI_API_KEY_VALUE')
if not api_key:
    raise Exception("API Key not found. Please set the 'OPENAI_API_KEY_VALUE' environment variable.")

# Setting the API Key for OpenAI
openai.api_key = api_key

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Adjust the model here as needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("Error during API call:", str(e))

# Example prompt
prompt = "Explain the importance of context in prompt engineering and provide techniques for effective prompt engineering."

# Generate response
response = generate_response(prompt)
if response:
    print(response)
else:
    print("No response generated.")