import pandas as pd
from datetime import datetime, timedelta
import requests


def get_candles(
    self,
    instrument_id: str,
    start_date: str,
    end_date: str,
    interval: str = "CANDLE_INTERVAL_5_MIN",
    is_complete: bool = True,
) -> pd.DataFrame:

    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"

    payload = {
        "from": start_date,
        "to": end_date,
        "interval": interval,
        "instrumentId": instrument_id,
        "candleSourceType": "CANDLE_SOURCE_UNSPECIFIED",
    }

    response = requests.post(url, headers=self.request_headers, json=payload)
    response.raise_for_status()  # check for errors

    # Convert response to DataFrame
    candles = response.json()["candles"]
    data = []

    for candle in candles:
        if not is_complete or candle["isComplete"]:
            data.append(
                {
                    "DATE": (
                        datetime.strptime(candle["time"], "%Y-%m-%dT%H:%M:%SZ")
                        + timedelta(hours=3)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "OPEN": float(candle["open"]["units"])
                    + float(candle["open"]["nano"]) / 1e9,
                    "HIGH": float(candle["high"]["units"])
                    + float(candle["high"]["nano"]) / 1e9,
                    "LOW": float(candle["low"]["units"])
                    + float(candle["low"]["nano"]) / 1e9,
                    "CLOSE": float(candle["close"]["units"])
                    + float(candle["close"]["nano"]) / 1e9,
                    "VOLUME": candle["volume"],
                }
            )

    return pd.DataFrame(data)
