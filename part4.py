import time
import logging
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_crypto_response(data):
    """Validate crypto API response structure."""
    try:
        quotes = data["quotes"]
        usd = quotes["USD"]

        required_fields = ["price", "percent_change_24h"]
        for field in required_fields:
            if field not in usd:
                return False, f"Missing field: {field}"

        return True, None

    except KeyError as e:
        return False, f"Missing key: {e}"



def safe_api_request(url, timeout=5, retries=3):
    """Make an API request with retries, logging, and full error handling."""

    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Attempt {attempt} - Requesting: {url}")

            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                logging.error("Invalid JSON response")
                return {"success": False, "error": "Invalid JSON response"}

            logging.info("Request successful")
            return {"success": True, "data": data}

        except (ConnectionError, Timeout) as e:
            logging.warning(f"Network issue on attempt {attempt}: {e}")
            if attempt == retries:
                return {
                    "success": False,
                    "error": f"Failed after {retries} attempts due to network issues"
                }
            time.sleep(1)

        except HTTPError as e:
            logging.error(f"HTTP Error {e.response.status_code}")
            return {
                "success": False,
                "error": f"HTTP Error: {e.response.status_code}"
            }

        except RequestException as e:
            logging.error(f"Request failed: {e}")
            return {
                "success": False,
                "error": f"Request failed: {e}"
            }


def fetch_crypto_safely():
    coin = input("Enter coin (btc-bitcoin, eth-ethereum): ").strip().lower()

    if not coin:
        print("Error: Coin name required.")
        return

    url = f"https://api.coinpaprika.com/v1/tickers/{coin}"
    result = safe_api_request(url)

    if not result["success"]:
        print(f"Error: {result['error']}")
        return

    data = result["data"]
    valid, error = validate_crypto_response(data)

    if not valid:
        print(f"Invalid API response: {error}")
        return

    usd = data["quotes"]["USD"]
    print(f"\n{data['name']} ({data['symbol']})")
    print(f"Price: ${usd['price']:,.2f}")
    print(f"24h Change: {usd['percent_change_24h']:+.2f}%")
