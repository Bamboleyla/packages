import requests
import uuid


def post_stop_order(
    self,
    stop_order_type: str,
    instrument_id: str,
    quantity: int,
    price: float,
    direction: str,
):
    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.StopOrdersService/PostStopOrder"

    payload = {
        "quantity": quantity,
        "stop_price": {"units": int(price), "nano": int((price - int(price)) * 1e9)},
        "direction": direction,
        "accountId": self.account_id,
        "expirationType": "STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL",
        "stopOrderType": stop_order_type,
        "instrumentId": instrument_id,
        "orderId": str(uuid.uuid4()),
    }

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()
    return response.json()
