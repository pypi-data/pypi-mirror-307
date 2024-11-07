from typing_extensions import TypedDict

from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_parameters import ToolParameters


class ToolData(TypedDict):
    """
        Represents the data returned as the response to a tool request.

        Attributes:
            tool_request_guid (str): A globally unique identifier for the tool data response.
            tool_data_class (str): The class of the tool data response.
            tool_name (str): The name of the tool that produced the tool data response.
            tool_parameters (ToolParameters): The parameters of calling the tool.
    """

    tool_request_guid: str
    tool_data_class: str
    tool_name: str
    tool_parameters: ToolParameters
