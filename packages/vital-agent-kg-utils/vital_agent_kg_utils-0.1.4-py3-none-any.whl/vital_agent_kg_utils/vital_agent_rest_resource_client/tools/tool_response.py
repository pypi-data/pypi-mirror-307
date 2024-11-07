from typing_extensions import TypedDict

from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_parameters import ToolParameters
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_results import ToolResults


class ToolResponse:
    tool_name: str
    tool_parameters: ToolParameters
    tool_results: ToolResults

    def __init__(self, tool_name: str, tool_parameters: ToolParameters, tool_results: ToolResults):
        self.tool_name = tool_name
        self.tool_parameters = tool_parameters
        self.tool_results = tool_results



