import requests



def fetch_dexscreener_data():
    url = "https://api.dexscreener.com/token-profiles/latest/v1"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    coins = []

    for token in data:
        if isinstance(token, dict):
            coins.append({
                "id": token.get("tokenAddress", "unknown"),
                "name": token.get("description", "Unknown Token"),
                "symbol": token.get("tokenAddress", "UNKNOWN")[:6].upper(),
                "url": token.get("url", ""),
                "chain": token.get("chainId", ""),
                "icon": token.get("icon", ""),
                "source": "dexscreener",
                "links": token.get("links", [])
            })
    print(f"Успешно обработано {len(coins)} токенов")
    return coins


def fetch_pumpfun_data():
    url = "https://api.pumpfun.io/coins"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    coins = []

    for token in data.get("coins", []):
        coins.append({
            "id": token["address"],
            "name": token["name"],
            "symbol": token["symbol"],
            "price_usd": float(token["price_usd"]),
            "volume_usd": float(token["volume_usd"]),
            "source": "pumpfun",
            "developer": token.get("creator", "unknown")
        })

    return coins
fetch_dexscreener_data()