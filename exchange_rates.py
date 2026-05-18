"""
exchange_rates.py
-----------------
Pulls live currency exchange rates from the Open Exchange Rates API (free tier)
and displays them in a clean, readable format.

Demonstrates:
- Making REST API calls with Python (requests library)
- Parsing JSON responses
- Handling HTTP errors gracefully

Usage:
    python exchange_rates.py
    python exchange_rates.py --base EUR
    python exchange_rates.py --base USD --currencies GBP EUR JPY CAD

Requirements:
    pip install requests
"""

import requests
import argparse
import json
from datetime import datetime


# Free public API - no key required for this endpoint
BASE_URL = "https://open.er-api.com/v6/latest"


def get_exchange_rates(base_currency="USD", target_currencies=None):
    """
    Fetch exchange rates from the API.
    
    Args:
        base_currency (str): The base currency code (e.g. USD, EUR, GBP)
        target_currencies (list): Optional list of currency codes to filter results
    
    Returns:
        dict: Parsed JSON response from the API, or None on failure
    """
    url = f"{BASE_URL}/{base_currency.upper()}"
    
    print(f"\nFetching exchange rates for base currency: {base_currency.upper()}")
    print(f"Endpoint: {url}\n")

    try:
        response = requests.get(url, timeout=10)
        
        # Raise an exception for bad HTTP status codes (4xx, 5xx)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("result") != "success":
            print(f"API returned an error: {data.get('error-type', 'Unknown error')}")
            return None
            
        return data

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Connection error - check your internet connection.")
    except requests.exceptions.Timeout:
        print("Request timed out - the API took too long to respond.")
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong with the request: {e}")
    
    return None


def display_rates(data, target_currencies=None):
    """
    Print exchange rates in a clean, readable format.
    
    Args:
        data (dict): Parsed API response
        target_currencies (list): Optional list of currencies to display
    """
    base = data["base_code"]
    rates = data["rates"]
    last_updated = data.get("time_last_update_utc", "Unknown")

    print("=" * 50)
    print(f"  Exchange Rates — Base Currency: {base}")
    print(f"  Last Updated: {last_updated}")
    print("=" * 50)

    if target_currencies:
        # Filter to only the currencies the user asked for
        filtered = {k: v for k, v in rates.items() if k in [c.upper() for c in target_currencies]}
        if not filtered:
            print("None of the requested currencies were found in the response.")
            return
        display_dict = filtered
    else:
        # Default: show a useful subset of common currencies
        common = ["EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "MXN", "INR", "BRL"]
        display_dict = {k: rates[k] for k in common if k in rates}

    for currency, rate in sorted(display_dict.items()):
        print(f"  {base} → {currency:<6}  {rate:>12.4f}")

    print("=" * 50)
    print(f"\n  {len(display_dict)} currencies displayed.")
    print(f"  Full response contained {len(rates)} currencies.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display live currency exchange rates."
    )
    parser.add_argument(
        "--base",
        default="USD",
        help="Base currency code (default: USD)"
    )
    parser.add_argument(
        "--currencies",
        nargs="+",
        help="Specific currencies to display (e.g. --currencies GBP EUR JPY)"
    )
    args = parser.parse_args()

    data = get_exchange_rates(base_currency=args.base)
    
    if data:
        display_rates(data, target_currencies=args.currencies)
    else:
        print("Could not retrieve exchange rate data.")


if __name__ == "__main__":
    main()
