import requests

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


def trigger_bonkbot_trade(config, coin):
    if not config["auto_trade_enabled"]:
        return

    # Формируем команду для BonkBot
    msg = f"/buy {coin['id']} {config['trade_amount_sol']}sol"

    # Отправляем команду через Telegram
    send_telegram_message(
        config["telegram_bot_token"],
        config["telegram_chat_id"],
        f"{config['bonkbot_username']} {msg}"
    )
