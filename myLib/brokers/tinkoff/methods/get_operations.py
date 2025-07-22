import requests


def get_operations(
    self,
    figi: str,
    from_date: str,
):
    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.OperationsService/GetOperations"

    payload = {"accountId": self.account_id, "figi": figi, "from": from_date}

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()
    return response.json()
