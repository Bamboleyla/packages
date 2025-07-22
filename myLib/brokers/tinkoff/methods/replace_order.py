import requests
import uuid
from time import time


def replace_order(
    self,
    order_id: str,
    instrument_id: str,
    quantity: int,
    price: float,
):
    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.OrdersService/ReplaceOrder"

    payload = {
        "accountId": self.account_id,
        "orderId": order_id,
        "idempotencyKey": f"{instrument_id}-{int(time())}-{uuid.uuid4().hex[:8]}",
        "quantity": quantity,
        "price": {"units": int(price), "nano": int((price - int(price)) * 1e9)},
    }

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()
    return response.json()
