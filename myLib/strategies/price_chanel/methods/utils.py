def get_open_position(self):
    portfolio = self._broker.get_portfolio()
    long_position = None
    short_position = None

    # Identify positions
    for p in portfolio["positions"]:
        if p["figi"] == self._figi and not p["blocked"]:
            units = int(p["quantity"]["units"])
            if units > 0:
                long_position = p
            elif units < 0:
                short_position = p
    return long_position, short_position


def get_indicator_name(self):
    pc_period, st_period, st_multiplier = self.get_indicators_params()

    # Indicator name constants
    ST_LOWER = f"ST_LOWER_{st_period}_{st_multiplier}"
    ST_UPPER = f"ST_UPPER_{st_period}_{st_multiplier}"
    PC_LOW = f"PC_{pc_period}_LOW"
    PC_HIGH = f"PC_{pc_period}_HIGH"

    return ST_LOWER, ST_UPPER, PC_LOW, PC_HIGH


def cancel_all_orders(self, orders):
    """Cancel all active orders"""
    for order in orders:
        self._broker.cancel_order(order["orderId"])


def replace_order_if_needed(self, order, new_price):
    """Replace order if price has changed"""
    if order is None:
        return None
    current_price = extract_price_from_dict(order["initialSecurityPrice"])
    if round(current_price, 2) != round(new_price, 2):
        return self._broker.replace_order(
            order_id=order["orderId"],
            instrument_id=order["instrumentUid"],
            quantity=order["lotsRequested"],
            price=new_price,
        )
    return order


def extract_price_from_dict(value: dict) -> float:
    return round(float(value["units"]) + float(value["nano"]) / 1e9, 2)
