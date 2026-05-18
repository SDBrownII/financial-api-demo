Exchange Rate Fetcher
A simple Python script that pulls live currency exchange rates from a public REST API and displays them in a clean, readable format.
What it demonstrates
Making REST API calls using Python's `requests` library
Parsing and working with JSON responses
Handling HTTP errors and edge cases gracefully (timeouts, bad status codes, connection errors)
Using command-line arguments to make the script flexible
Requirements
```
pip install requests
```
Usage
Basic — show common currencies against USD:
```
python exchange_rates.py
```
Change the base currency:
```
python exchange_rates.py --base EUR
```
Show only specific currencies:
```
python exchange_rates.py --base USD --currencies GBP EUR JPY CAD
```
Example output
```
Fetching exchange rates for base currency: USD
Endpoint: https://open.er-api.com/v6/latest/USD

==================================================
  Exchange Rates — Base Currency: USD
  Last Updated: Thu, 15 May 2026 00:02:01 +0000
==================================================
  USD → AUD        1.5412
  USD → BRL        5.1830
  USD → CAD        1.3601
  USD → CHF        0.9012
  USD → CNY        7.2410
  USD → EUR        0.9201
  USD → GBP        0.7893
  USD → INR       83.4500
  USD → JPY      154.2300
  USD → MXN       17.1240
==================================================

  10 currencies displayed.
  Full response contained 162 currencies.
```
API
Uses the free Open Exchange Rates API — no API key required for the `/latest` endpoint.
