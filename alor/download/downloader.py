"""Main class for downloading Alor data"""

import logging
from datetime import datetime
import asyncio
import pandas as pd


from .api import AlorAPI


logger = logging.getLogger("AlorDownloader")

alor_api = AlorAPI()


class AlorDownloader:
    """This class downloads and saves Alor data."""

    def get_quotes(self, ticker: str, start_date: datetime, tf: int) -> pd.DataFrame:
        """method return"""
        return asyncio.run(
            alor_api.get_ticker_data(ticker=ticker, start_date=start_date, tf=tf)
        )
