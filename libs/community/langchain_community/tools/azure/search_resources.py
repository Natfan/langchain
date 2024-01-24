"""Util that Searches resources in Azure.

Free, but setup is required. See link below.
https://learn.microsoft.com/en-us/graph/auth
"""

from datetime import datetime as dt
from typing import Any, Dict, List, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Extra, Field

from langchain_community.tools.office365.base import O365BaseTool
from langchain_community.tools.office365.utils import UTC_FORMAT, clean_body


class SearchResourcesInput(BaseModel):
    """Input for SearchEmails Tool.

    From https://learn.microsoft.com/en-us/graph/search-query-parameter"""

    resource_type: str = Field(
        description=(
            " The type of the resource for the search query in the following format: "
            ' Provider.Type, where "Provider" is usually "Microsoft" and the type is the'
            ' short name for the resource, such as Logic Apps being "Microsoft.Logic".'
        )
    )
    resource_group_name: str = Field(
        description=(
            " The name of the resource group that contains the resources. A free-form text field, "
            " with the following restrictions: "
            " * 1 to 90 characters "
            " * May contain letters, digits, paraentheses, periods, hyphens and underscopes. "
        )
    )
    resource_name: str = Field(
        description=(
            " The optional name of the resource. A free-form text field that can be anything, but is "
            " likely alphanumeric text, potentially with hyphens or underscores. "
        )
    )
    max_results: int = Field(
        default=10,
        description="The maximum number of results to return.",
    )
    truncate: bool = Field(
        default=True,
        description=(
            "Whether the event's body is truncated to meet token number limits. Set to "
            "False for searches that will retrieve small events, otherwise, set to "
            "True."
        ),
    )


class AzureSearchResources(AzureBaseTool):
    """Class for searching resources in Azure

    Free, but setup is required
    """

    name: str = "resource_search"
    args_schema: Type[BaseModel] = SearchResourcesInput
    description: str = (
        " Use this tool to search for the resources in Azure."
        " The input must be the type of resources for the query, along with the Resource "
        " Group Name. Optionally, the name of the resource will be provided, but "
        " potentially only a bit of it, so perform fuzzy matching where appropriate."
        " The output is a JSON list of all the resources of that specific type in the resource group"
    )

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def _run(
        self,
        resource_type: str,
        resource_group_name: str,
        resource_name: str,
        max_results: int = 10,
        truncate: bool = True,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        truncate_limit: int = 150,
    ) -> List[Dict[str, Any]]:
        # Get resource objects
        resource_group = self.resource_client.resource_groups.get(resource_group_name)
        resources = self.resource_client.resources.list_by_resource_group(resource_group)

        # Generate output dict
        output_resources = []
        for resource in resources:
            output_resource = {}
            output_resource["organizer"] = resource.organizer

            output_resource["subject"] = resource.subject

            if truncate:
                output_resource["body"] = clean_body(resource.body)[:truncate_limit]
            else:
                output_resource["body"] = clean_body(resource.body)

            # Get the time zone from the search parameters
            time_zone = start_datetime_query.tzinfo
            # Assign the datetimes in the search time zone
            output_resource["start_datetime"] = resource.start.astimezone(time_zone).strftime(
                UTC_FORMAT
            )
            output_resource["end_datetime"] = resource.end.astimezone(time_zone).strftime(
                UTC_FORMAT
            )
            output_resource["modified_date"] = resource.modified.astimezone(
                time_zone
            ).strftime(UTC_FORMAT)

            output_resources.append(output_resource)

        return output_resources
