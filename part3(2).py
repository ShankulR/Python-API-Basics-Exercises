import requests

def search_todos():
    print("\n--- Todos---")
    print("'True' for completed tasks")
    print("'False for incomplete tasks")

    status = input("Status(true / false): ").lower().strip()

    if status not in ["true", "false"]:
        print("Enter 'true' or 'false'")
        return

    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url, params={"completed": status})
    todos = response.json()

    print(f"\nFound {len(todos)} tasks with completed = {status}\n")

    for i, todo in enumerate(todos[:15], 1):  
        print(f"{i}. {todo['title']}")
        
search_todos()