import pandas as pd
from .utils import (
    cancel_all_orders,
    get_indicator_name,
    get_open_position,
    replace_order_if_needed,
    extract_price_from_dict,
)


def run(self, data: pd.DataFrame) -> pd.DataFrame:
    long_position, short_position = get_open_position(self)

    # Initialize from_date if no positions
    if long_position is None and short_position is None:
        self.from_date = pd.Timestamp.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    orders = self._broker.get_orders(figi=self._figi)

    if len(orders) == 0:
        self._order = None
        self._take_profit = None
        self._stop_loss = None
    elif self._order is None and self._take_profit is None and self._stop_loss is None:
        cancel_all_orders(self, orders)
        orders = []

    previous = data.iloc[-2]

    ST_LOWER, ST_UPPER, PC_LOW, PC_HIGH = get_indicator_name(self)

    # Handle LONG position logic
    def handle_long_position():
        """Operations for long positions"""
        # Close short position if exists
        if short_position is not None:
            self._broker.create_market_buy_order(
                instrument_id=short_position["figi"],
                quantity=extract_price_from_dict(short_position["quantityLots"]) * -1,
            )
            self._order = None
            self._take_profit = None
            self._stop_loss = None
            return

        # No open long position
        if long_position is None:
            if len(orders) == 0:
                if previous[ST_LOWER] < previous[PC_LOW]:
                    self._order = self._broker.create_limit_buy_order(
                        instrument_id=self._figi, price=previous[PC_LOW], quantity=1
                    )
            elif self._order is not None:
                if previous[ST_LOWER] < previous[PC_LOW]:
                    self._order = replace_order_if_needed(
                        self, self._order, previous[PC_LOW]
                    )
                elif previous[ST_LOWER] > previous[PC_LOW]:
                    cancel_all_orders(self, orders)

            else:
                raise Exception("Unexpected state B220725")

        # Existing long position
        else:
            # Find last executed buy operation
            operations = self._broker.get_operations(self._figi, self._from_date)[
                "operations"
            ]
            executed_buys = [
                op
                for op in operations
                if op["state"] == "OPERATION_STATE_EXECUTED"
                and op["operationType"] == "OPERATION_TYPE_BUY"
            ]
            executed_buys.sort(key=lambda x: x["date"])

            last_buy_price = extract_price_from_dict(executed_buys[-1]["price"])

            if (
                self._order is None
                and previous[ST_LOWER] < previous[PC_LOW]
                and previous[PC_LOW] < last_buy_price
            ):
                self._order = self._broker.create_limit_buy_order(
                    instrument_id=self._figi, price=previous[PC_LOW], quantity=1
                )

            elif int(long_position["quantityLots"]["units"]) > 1:
                stop_price = round(
                    extract_price_from_dict(long_position["averagePositionPrice"])
                    * 1.001,
                    2,
                )
                if self._reducing_position_order is None:
                    self._reducing_position_order = (
                        self._broker.create_limit_sell_order(
                            instrument_id=self._figi,
                            price=stop_price,
                            quantity=int(long_position["quantityLots"]["units"]) - 1,
                        )
                    )
                else:
                    reducing_position_order_price = extract_price_from_dict(
                        self._reducing_position_order["initialSecurityPrice"]
                    )
                    if reducing_position_order_price != stop_price or int(
                        long_position["quantityLots"]["units"]
                    ) - 1 != int(self._reducing_position_order["lotsRequested"]):
                        self._broker.cancel_order(
                            self._reducing_position_order["orderId"]
                        )
                        self._reducing_position_order = (
                            self._broker.create_limit_sell_order(
                                instrument_id=self._figi,
                                price=stop_price,
                                quantity=int(long_position["quantityLots"]["units"])
                                - 1,
                            )
                        )

            # Manage take profit order
            take_profit_price = previous[PC_HIGH]
            if self._take_profit is None:
                self._take_profit = self._broker.create_limit_sell_order(
                    instrument_id=self._figi, price=take_profit_price, quantity=1
                )
            else:
                self._take_profit = replace_order_if_needed(
                    self, self._take_profit, take_profit_price
                )

    # Handle SHORT position logic
    def handle_short_position():
        """Operations for short positions"""
        # Close long position if exists
        if long_position is not None:
            self._broker.create_market_sell_order(
                instrument_id=long_position["figi"],
                quantity=extract_price_from_dict(long_position["quantityLots"]),
            )
            self._order = None
            self._take_profit = None
            self._stop_loss = None
            return

        # No open short position
        if short_position is None:
            if len(orders) == 0:
                if previous[ST_UPPER] > previous[PC_HIGH]:
                    self._order = self._broker.create_limit_sell_order(
                        instrument_id=self._figi, price=previous[PC_HIGH], quantity=1
                    )
            elif self._order is not None:
                if previous[ST_UPPER] > previous[PC_HIGH]:
                    self._order = replace_order_if_needed(
                        self, self._order, previous[PC_HIGH]
                    )
                elif previous[ST_UPPER] < previous[PC_HIGH]:
                    cancel_all_orders(self, orders)
            else:
                raise Exception("Unexpected state A220725")

        # Existing short position
        else:
            # Get last sell operation
            operations = self._broker.get_operations(self._figi, self._from_date)[
                "operations"
            ]
            executed_sells = [
                op
                for op in operations
                if op["state"] == "OPERATION_STATE_EXECUTED"
                and op["operationType"] == "OPERATION_TYPE_SELL"
            ]
            executed_sells.sort(key=lambda x: x["date"])
            last_sell_price = extract_price_from_dict(executed_sells[-1]["price"])

            if (
                previous[ST_UPPER] > previous[PC_HIGH]
                and previous[PC_HIGH] > last_sell_price
            ):
                self._order = self._broker.create_limit_sell_order(
                    instrument_id=self._figi,
                    price=previous[PC_HIGH],
                    quantity=1,
                )
            elif int(short_position["quantityLots"]["units"]) < -1:
                for sell in executed_sells:
                    stop_price = round(extract_price_from_dict(sell["price"]) * 0.999)
                    if not any(
                        extract_price_from_dict(order["initialSecurityPrice"])
                        == stop_price
                        for order in orders
                    ):

                        self._broker.create_limit_buy_order(
                            instrument_id=self._figi,
                            price=stop_price,
                            quantity=1,
                        )

            # Manage take profit order
            take_profit_price = previous[PC_LOW]
            if self._take_profit is None:
                self._take_profit = self._broker.create_limit_buy_order(
                    instrument_id=self._figi, price=take_profit_price, quantity=1
                )
            else:
                self._take_profit = replace_order_if_needed(
                    self, self._take_profit, take_profit_price
                )

    # Main trend handling logic
    if pd.notna(previous[ST_LOWER]):
        handle_long_position()
    elif pd.notna(previous[ST_UPPER]):
        handle_short_position()
    else:
        raise ValueError("Trend direction cannot be determined")
