"""This module provides functionality for managing Alor API tokens."""

import json
import logging
import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("AlorToken")

# Load configuration
alor_config = json.loads(os.getenv("ALOR", "{}"))  # Added default value


def get_access_token(payload):
    """This function sends a POST request to the ALOR OAuth endpoint to get an access token."""
    response = requests.post(
        url=f"{alor_config['url_oauth']}/refresh",
        data=payload,
        timeout=5,
    )
    response.raise_for_status()  # Call httperror for 4xx/5xx statuses

    res_json = response.json()
    access_token: str = res_json.get("AccessToken")
    if not access_token:
        logger.error("AccessToken not found in the response.")
        return None

    masked_token = f"{access_token[:4]}...{access_token[-4:]}"
    logger.info("JWT received: %s", masked_token)
    return {
        "access_token": access_token,
        "created_at": int(datetime.now().timestamp()),
    }
