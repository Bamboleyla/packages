import requests


def get_orders(self):
    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.OrdersService/GetOrders"

    payload = {"accountId": self.account_id}

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()
    return response.json()
