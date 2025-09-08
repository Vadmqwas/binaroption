import time, yaml
from modules.storage import Database
from modules.fetchers import fetch_dexscreener_data, fetch_pumpfun_data
from modules.filters import filter_coins
from modules.detection import detect_events
from modules.telegram import send_telegram_message, trigger_bonkbot_trade


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    db = Database(config["database_path"])

    while True:
        # Получение данных с Dexscreener и Pumpfun
        coins = fetch_dexscreener_data() + fetch_pumpfun_data()

        # Фильтрация монет
        coins = filter_coins(coins, config)

        # История из БД
        past = db.fetch_all()

        # Детекция событий (pump/rug/tier1)
        events = detect_events(coins, past, config)

        # Сохраняем монеты
        for coin in coins:
            db.insert_coin(coin)

        # Обрабатываем события
        for ev_type, coin in events:
            msg = f"[{ev_type.upper()}] {coin['name']} ({coin['symbol']}) at ${coin['price_usd']}"
            send_telegram_message(
                config["telegram_bot_token"],
                config["telegram_chat_id"],
                msg
            )
            if ev_type == "pump":
                trigger_bonkbot_trade(config, coin)
        # Ждём перед следующим циклом
        time.sleep(config["fetch_interval_seconds"])


if __name__ == "__main__":
    main()
