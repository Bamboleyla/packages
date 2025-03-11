"""Main class for downloading Alor data"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
import pandas as pd
from dotenv import load_dotenv

from .api import AlorAPI


logger = logging.getLogger("AlorDownloader")

load_dotenv()

alor_config = json.loads(os.getenv("ALOR"))  # Load configuration
alor_api = AlorAPI()


class AlorDownloader:
    """This class downloads and saves Alor data."""

    async def prepare(self):
        """This method prepares necessary directories and files."""
        percent_step = 100 / len(alor_config["tickers"])  # initial percentage
        percentage = 0.0  # complete percentage
        for ticker in alor_config["tickers"]:
            ticker_dir = os.path.join("alor", "tickers", ticker)
            # Check ticker directory
            if not os.path.exists(ticker_dir):
                # Create ticker directory
                os.makedirs(ticker_dir)
                logger.info("Created directory for %s", ticker)

            file_path_to_quotes = os.path.join(
                "alor", "tickers", ticker, "quotes.csv"
            )  # Path to quotes file

            # **CREATE OR UPDATE QUOTES**

            # Check if quotes file exists
            if not os.path.exists(file_path_to_quotes):

                now = datetime.now(timezone.utc)  # Get current date and time
                one_month_ago = now - timedelta(
                    days=31
                )  # Subtract approximately 1 month ago
                first_day_of_month = one_month_ago.replace(
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                    tzinfo=timezone(timedelta(hours=3)),
                )  # Get first day of current month

                quotes = await alor_api.get_ticker_data(
                    ticker=ticker, start_date=first_day_of_month, tf=300
                )  # Get quotes for period

                # Check if quotes is not empty
                if not quotes.empty:
                    quotes.to_csv(
                        file_path_to_quotes, index=False
                    )  # save quotes to file
                    logger.info("Created quotes file for %s", ticker)
                else:
                    logger.info("No data for %s in the last month", ticker)

            # Update quotes
            else:
                quotes = pd.read_csv(file_path_to_quotes)  # Read file with quotes

                last_write_date = datetime.strptime(
                    quotes.iloc[-1]["DATE"], "%Y%m%d %H:%M:%S"
                ).replace(
                    tzinfo=timezone(timedelta(hours=3))
                )  # Get last write date
                if (
                    quotes.iloc[0]["TICKER"] != "SBER"
                    and (datetime.now(timezone.utc) - last_write_date).days < 7
                ):
                    percentage += percent_step
                    print(
                        f"Loading {ticker} quotes was skipped, {percentage:.2f}% completed"
                    )
                    continue  # Skip if last write date is less than 7 days ago

                new_quotes = await alor_api.get_ticker_data(
                    ticker=ticker, start_date=last_write_date, tf=300
                )
                # Get new quotes for period
                quotes = pd.concat(
                    [quotes.iloc[:-1], new_quotes]
                )  # Combine quotes and new quotes into one DataFrame
                quotes.to_csv(file_path_to_quotes, index=False)  # save quotes to file

                logger.info("Updated quotes file for %s", ticker)

            percentage += percent_step
            print(f"Downloaded {ticker} quotes, {percentage:.2f}% completed")
