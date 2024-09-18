import requests

url = "https://staging.dev.api.epam.com/info/datasets"

response = requests.get(url)

if response.status_code == 200:
    print("Success!")
    print(response.json())
else:
    print(f"Failed to retrieve data: {response.status_code}")