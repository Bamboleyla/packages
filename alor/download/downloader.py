"""Main class for downloading Alor data"""

import json
import logging
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from .api import AlorAPI


logger = logging.getLogger("AlorDownloader")

load_dotenv()

alor_config = json.loads(os.getenv("ALOR"))  # Load configuration
alor_api = AlorAPI()


class AlorDownloader:
    """This class downloads and saves Alor data."""

    async def get_quotes(
        self, ticker: str, start_date: datetime, tf: int
    ) -> pd.DataFrame:
        """method return"""
        return await alor_api.get_ticker_data(
            ticker=ticker, start_date=start_date, tf=tf
        )
