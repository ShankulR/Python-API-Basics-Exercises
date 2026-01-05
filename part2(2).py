import requests

url = "https://jsonplaceholder.typicode.com/users/5"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Found")
    print(data)
else:
    print("Not Found")