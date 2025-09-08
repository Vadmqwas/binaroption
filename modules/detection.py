def detect_events(current_coins, past_coins, config):
    events = []
    past_lookup = {c[0]: c for c in past_coins}

    for coin in current_coins:
        old = past_lookup.get(coin["id"])
        if old:
            old_price = old[3]
            if old_price > 0:
                price_change = ((coin["price_usd"] - old_price) / old_price) * 100
                if price_change >= config["pump_percentage"]:
                    events.append(("pump", coin))

                drop = ((old_price - coin["price_usd"]) / old_price) * 100
                if drop >= config["rug_drop_percentage"]:
                    events.append(("rug", coin))

        if coin["volume_usd"] >= config["tier1_volume_usd"]:
            events.append(("tier1", coin))

    return events
