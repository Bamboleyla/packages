import pandas as pd
import os
from datetime import datetime, timedelta
import requests

__all__ = ["Tinkoff"]


class Tinkoff:
    """Represents a Tinkoff broker."""

    def __init__(self):
        self.name = "Tinkoff"
        self.token = os.getenv("TINKOFF_TOKEN")

    def get_candles(
        self,
        instrument_id: str,
        start_date: str,
        end_date: str,
        interval: str = "CANDLE_INTERVAL_5_MIN",
        is_complete: bool = True,
    ) -> pd.DataFrame:
        """
        Retrieves candle data from Tinkoff Invest API

        Parameters:
            instrument_id (str): FIGI of the instrument
            start_date (str): Start date in format "%Y-%m-%dT%H:%M:%S.%fZ"
            end_date (str): End date in format "%Y-%m-%dT%H:%M:%S.%fZ"
            interval (str): Candle interval (default: 5 minutes)
            is_complete (bool): If True, returns only complete candles

        Returns:
            pd.DataFrame: DataFrame with candle data
        """
        url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",  # token is expected to be stored in broker
            "Content-Type": "application/json",
        }

        payload = {
            "from": start_date,
            "to": end_date,
            "interval": interval,
            "instrumentId": instrument_id,
            "candleSourceType": "CANDLE_SOURCE_UNSPECIFIED",
        }

        response = requests.post(url, headers=headers, json=payload)
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
