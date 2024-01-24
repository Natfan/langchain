"""Azure tool utils."""
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

# if TYPE_CHECKING:
#     from O365 import Account

logger = logging.getLogger(__name__)


def clean_body(body: str) -> str:
    """Clean body of a message or event."""
    try:
        from bs4 import BeautifulSoup

        try:
            # Remove HTML
            soup = BeautifulSoup(str(body), "html.parser")
            body = soup.get_text()

            # Remove return characters
            body = "".join(body.splitlines())

            # Remove extra spaces
            body = " ".join(body.split())

            return str(body)
        except Exception:
            return str(body)
    except ImportError:
        return str(body)


def authenticate() -> ResourceManagementClient:
    if "AZURE_SUBSCRIPTION_ID" is not os.environ:
        raise ValueError("The 'AZURE_SUBSCRIPTION_ID' environment variable is not set.")
    return ResourceManagementClient(AzureCliCredential(), os.environ["AZURE_SUBSCRIPTION_ID"])


UTC_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""UTC format for datetime objects."""
