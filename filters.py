from modules.fake_volume import is_fake_volume
from modules.rugcheck import check_rugcheck

def filter_coins(coins, config):
    filtered = []
    for coin in coins:
        # Проверка по чёрным спискам
        if coin["id"] in config["coin_blacklist"]:
            continue
        if coin["links"] in config["developer_blacklist"]:
            continue

        # Проверка по диапазону цены
        if not (config["min_price_usd"] <= coin["price_usd"] <= config["max_price_usd"]):
            continue

        # Проверка на фейковый объём
        if is_fake_volume(coin, config):
            continue

        # Проверка через RugCheck
        rc = check_rugcheck(coin["id"], config)

        if config["rugcheck"]["block_if_not_good"] and rc["status"] != "Good":
            continue

        if config["rugcheck"]["block_if_bundled_supply"] and rc["bundled"]:
            # Автоматически добавляем в блэклисты
            config["coin_blacklist"].append(coin["id"])
            config["developer_blacklist"].append(coin["developer"])
            continue

        filtered.append(coin)

    return filtered
