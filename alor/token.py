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

import json
import logging
import os
from datetime import datetime
from json import JSONDecodeError
from typing import Dict, Optional, Union
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("AlorToken")

# Load configuration
alor_config = json.loads(os.getenv("ALOR", "{}"))  # Добавлено значение по умолчанию


class AlorToken:
    """Class to get a JWT token from ALOR."""

    def get_access_token(self) -> Optional[Dict[str, Union[str, int]]]:
        """
        Get a JWT token from ALOR by using refresh token.

        The method makes a POST request to the ALOR service with the refresh
        token as a parameter. If the response is 200, it extracts the JWT token
        from the JSON response and returns it. If the response is not 200, it logs
        an error. If there is an error while decoding the JSON response, it logs an error.

        :return: A dictionary with keys "access_token" (str) and "created_at" (int), or None if an error occurred.
        """
        if not alor_config.get("token") or not alor_config.get("url_oauth"):
            logger.error("ALOR configuration is missing or incomplete.")
            return None

        payload = {"token": alor_config["token"]}

        try:
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

        except requests.exceptions.RequestException as e:
            logger.error("HTTP request failed: %s", e)
        except JSONDecodeError as e:
            logger.error("Failed to decode JSON response: %s", e)
        except KeyError as e:
            logger.error("Missing key in configuration: %s", e)

        return None
