import requests
import json
import os
from datetime import datetime


CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),

    # Added cities
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "kochi": (9.9312, 76.2673),
    "paris": (48.8566, 2.3522),
    "dubai": (25.2048, 55.2708),
}

CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
}


def get_weather(city):
    city = city.lower().strip()

    if city not in CITIES:
        print("City not found.")
        return None

    lat, lon = CITIES[city]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def display_weather(city):
    data = get_weather(city)
    if not data:
        return

    current = data["current_weather"]

    print("\n" + "=" * 40)
    print(f"Weather in {city.title()}")
    print("=" * 40)
    print(f"Temperature: {current['temperature']}°C")
    print(f"Wind Speed: {current['windspeed']} km/h")
    print("=" * 40)

    save_to_file(f"{city}_weather.json", data)



def get_crypto_price(coin):
    coin = coin.lower().strip()
    coin_id = CRYPTO_IDS.get(coin, coin)

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    return response.json()


def display_crypto(coin):
    data = get_crypto_price(coin)
    if not data:
        print("Crypto not found.")
        return

    usd = data["quotes"]["USD"]

    print("\n" + "=" * 40)
    print(f"{data['name']} ({data['symbol']})")
    print("=" * 40)
    print(f"Price: ${usd['price']:,.2f}")
    print(f"24h Change: {usd['percent_change_24h']:+.2f}%")
    print("=" * 40)

    save_to_file(f"{coin}_price.json", data)



def compare_cryptos(coins):
    print("\n" + "=" * 55)
    print(f"{'Crypto':<15}{'Price':<15}{'24h Change'}")
    print("=" * 55)

    for coin in coins:
        data = get_crypto_price(coin)
        if not data:
            continue

        usd = data["quotes"]["USD"]
        print(
            f"{data['name']:<15}"
            f"${usd['price']:>12,.2f}  "
            f"{usd['percent_change_24h']:+.2f}%"
        )


def create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "My Post",
        "body": "Learning APIs with Python",
        "userId": 1
    }

    response = requests.post(url, json=payload)
    print("\nPOST Response:")
    print(response.json())



def save_to_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def dashboard():
    print("\n" + "=" * 50)
    print("Real-World API Dashboard")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    while True:
        print("""
1. Check Weather
2. Check Crypto
3. Compare Cryptos
4. Create POST Request
5. Exit
""")

        choice = input("Select: ").strip()

        if choice == "1":
            print("Cities:", ", ".join(CITIES.keys()))
            city = input("City: ")
            display_weather(city)

        elif choice == "2":
            print("Cryptos:", ", ".join(CRYPTO_IDS.keys()))
            coin = input("Crypto: ")
            display_crypto(coin)

        elif choice == "3":
            coins = input("Enter coins (comma separated): ").split(",")
            compare_cryptos(coins)

        elif choice == "4":
            create_post()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    dashboard()
