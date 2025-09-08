import requests

def is_fake_volume(coin, config):
    # Быстрый фильтр по минимальному объёму
    if coin["volume_usd"] < config["min_volume_usd"]:
        return True

    # Проверка через Pocket Universe (если ключ задан)
    key = config.get("pocket_universe_api_key")
    if key:
        try:
            resp = requests.get(
                "https://api.pocketuniverse.app/verify_volume",
                params={"token": coin["id"], "apikey": key},
                timeout=5
            )
            if resp.ok and resp.json().get("fake"):
                return True
        except:
            pass

    return False
