import json

from typing_extensions import TypedDict
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_parameters import ToolParameters


class ToolRequest:
    tool: str
    tool_parameters: ToolParameters

    def __init__(self, tool: str, tool_parameters: ToolParameters):
        self.tool = tool
        self.tool_parameters = tool_parameters

    def to_dict(self) -> dict:
        """
        Converts ToolRequest instance to a dictionary.

        Returns:
            dict: The dictionary representation of the tool request.
        """
        return {
            "tool": self.tool,
            "tool_parameters": self.tool_parameters
        }
