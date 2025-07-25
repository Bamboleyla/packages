import requests


def cancel_order(self, order_id: str):
    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.OrdersService/CancelOrder"

    payload = {
        "accountId": self.account_id,
        "orderId": order_id,
    }

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()
    return response.json()
