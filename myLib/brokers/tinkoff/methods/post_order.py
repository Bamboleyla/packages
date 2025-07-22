import requests
import uuid
from time import time
from typing import Dict, Any


def post_order(
    self,
    order_type: str,
    instrument_id: str,
    quantity: int,
    direction: str,
    price: float | None,
) -> Dict[str, Any]:

    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.OrdersService/PostOrder"

    # Generate a unique order ID
    order_id = f"{instrument_id}-{int(time())}-{uuid.uuid4().hex[:8]}"

    # Base payload common to all orders
    payload = {
        "accountId": self.account_id,
        "orderType": order_type,
        "instrumentId": instrument_id,
        "quantity": str(
            quantity
        ),  # Convert to string as API often expects string numbers
        "direction": direction,
        "orderId": order_id,
        "timeInForce": "TIME_IN_FORCE_DAY",
    }

    # Add price details for limit orders
    if price is not None:
        payload["price"] = {
            "units": int(price),
            "nano": int((price - int(price)) * 1e9),
        }

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()
    return response.json()
