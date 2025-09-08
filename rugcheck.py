import requests

def check_rugcheck(token_address, config):
    try:
        url = f"{config['rugcheck']['api_url']}/{token_address}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        status = data.get("result", {}).get("risk", {}).get("status", "Unknown")
        bundled = data.get("result", {}).get("token", {}).get("bundled_supply", False)

        return {"status": status, "bundled": bundled}
    except:
        return {"status": "Unknown", "bundled": False}
