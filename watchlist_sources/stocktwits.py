import requests

def get_stocktwits_trending():
    url = "https://api.stocktwits.com/api/2/streams/trending.json"
    headers = {
        "User-Agent": "Mozilla/5.0",  # Trick the server into thinking you're a browser
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ StockTwits trending fetch failed: {response.status_code}")
        return []

    try:
        data = response.json()
        symbols = [message['symbols'][0]['symbol'] for message in data['messages'] if message['symbols']]
        return list(set(symbols))
    except (ValueError, KeyError, IndexError) as e:
        print(f"❌ Failed to parse StockTwits trending data: {e}")
        return []
