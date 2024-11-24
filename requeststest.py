import requests

# CoinGecko API URL
url = "https://api.coingecko.com/api/v3/simple/price"

# Define the parameters for the request (cryptocurrency IDs and currency)
params = {
    "ids": "bitcoin,ethereum",  # Cryptocurrency IDs, comma-separated
    "vs_currencies": "usd"      # Currency to convert to (e.g., USD)
}

# Set the headers for the request
headers = {
    "accept": "application/json"
}

# Send the GET request with parameters
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
