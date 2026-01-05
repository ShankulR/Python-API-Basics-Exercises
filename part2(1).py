def get_usr_phno(user_id):
    url = "https://jsonplaceholder.typicode.com/users/5"
    response = requests.get(url)

    data = response.json()

    print(f"userID:{data['id']} and phNo:{data['phone']}")
