"""Base class for Azure tools."""
from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool

from langchain_community.tools.azure.utils import authenticate

# if TYPE_CHECKING:
#     from O365 import Account


class AzureBaseTool(BaseTool):
    """Base class for the Azure tools."""

    resource_client: ResourceManagementClient = Field(default_factory=authenticate)
    """The account object for the Azure account."""
