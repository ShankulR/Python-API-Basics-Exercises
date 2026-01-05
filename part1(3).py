import requests
url = "https://jsonplaceholder.typicode.com/posts/999"
response = requests.get(url)
print("=== Basic API Request ===\n")
print(f"URL: {url}")
print(f"Status Code: {response.status_code}")
print(f"\nResponse Data:")
print(response.json())
