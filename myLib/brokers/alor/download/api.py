"""This class manages API for Alor brocker."""

import json
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
import pandas as pd
import websockets
from dotenv import load_dotenv
from ..__token import AlorToken

load_dotenv()

logger = logging.getLogger("AlorAPI")


class AlorAPI:
    """Manages the API for the Alor broker.

    This class handles authentication, websocket connections, and data retrieval
    from the Alor API.
    """

    def __init__(self):
        token = AlorToken()  # Load token service

        self.ws_url = os.getenv("ALOR_WEBSOCKET_URL")  # Get websocket url
        self.access_token = token.get_token()["access_token"]  # Get access token

    async def get_ticker_data(
        self, ticker: str, start_date: datetime, tf: int
    ) -> pd.DataFrame:
        """Retrieves ticker data from the Alor API.

        This method connects to the Alor WebSocket API, retrieves historical
        bar data for the specified ticker and timeframe, and returns it as a
        Pandas DataFrame.
        """
        df = pd.DataFrame(
            columns=["TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"],
        )  # Create quotes DataFrame

        async with websockets.connect(self.ws_url) as websocket:  # connect to websocket
            message = {
                "opcode": "BarsGetAndSubscribe",
                "code": ticker,
                "tf": tf,
                "from": start_date.timestamp(),
                "delayed": False,
                "skipHistory": False,
                "exchange": "MOEX",
                "format": "Simple",
                "frequency": 100,
                "guid": uuid.uuid4().hex,
                "token": self.access_token,
            }
            await websocket.send(json.dumps(message))  # send message
            # receive response
            while True:
                try:
                    response = await websocket.recv()  # receive response
                    response_dict = json.loads(
                        response
                    )  # convert response to dictionary

                    if (
                        "httpCode" in response_dict
                    ):  # check if response contains 'httpCode'
                        return df  # return responses because httpCode is last field in response

                    json_item = json.loads(response)["data"]  # convert item to json
                    date = (
                        datetime.fromtimestamp(json_item["time"], timezone.utc)
                        .astimezone(timezone(offset=timedelta(hours=3)))
                        .strftime("%Y%m%d %H:%M:%S")
                    )  # convert timestamp to datetime, then to local time (UTC+3)

                    df.loc[len(df)] = [
                        ticker,
                        date,
                        json_item["open"],
                        json_item["high"],
                        json_item["low"],
                        json_item["close"],
                        json_item["volume"],
                    ]  # add row to df

                except websockets.ConnectionClosed as e:
                    logger.error("WebSocket connection closed: %s", e)
                    break

        return df
