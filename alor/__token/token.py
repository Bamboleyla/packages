"""
This module contains the AlorToken class, which is used to get a JWT token from the ALOR broker.

The AlorToken class provides a method to retrieve an access token using a refresh token.
It handles HTTP requests to the ALOR OAuth endpoint and manages token retrieval and error handling.

Example usage:
    token_provider = AlorToken()
    token_data = token_provider.get_access_token()
    if token_data:
        print("Access Token:", token_data["access_token"])
    else:
        print("Failed to retrieve token.")
"""

import logging
import os
from typing import Dict, Optional, Union
import asyncio
from dotenv import load_dotenv


from .api import get_access_token

load_dotenv()

logger = logging.getLogger("AlorToken")


class AlorToken:
    """This class controls Alor tokens"""

    def get_token(self) -> Optional[Dict[str, Union[str, int]]]:
        """Get a JWT token from ALOR by using refresh token."""
        if not os.getenv("ALOR_TOKEN") or not os.getenv("ALOR_URL_OAUTH"):
            logger.error("ALOR configuration is missing or incomplete.")
            return None

        payload = {"token": os.getenv("ALOR_TOKEN")}

        return asyncio.run(get_access_token(payload))
