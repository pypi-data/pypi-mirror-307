import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager, wrapped_func


def ref_tools(tool_id):
    tool_base_path = "../../tool"
    module_path = os.path.join(tool_base_path, tool_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Tool {tool_id} not found")
        return []

    try:
        with ModuleManager(module_path) as manager:
            module = importlib.import_module("tool")
            export_tools = getattr(module, "export_tools")
            valid_tools = []
            for tool in export_tools:
                assert isinstance(tool, langchain_core.tools.StructuredTool) or isinstance(
                    tool, types.FunctionType
                ), f"Tool is not a StructuredTool or function: {tool}"
                if not isinstance(tool, langchain_core.tools.StructuredTool):
                    tool = to_agent_tool(tool)
                valid_tools.append(tool)
            export_tools = valid_tools

    except Exception as e:
        print(f"Error loading tool {tool_id}: {e}")
        return []

    for tool in export_tools:
        tool.func = wrapped_func(tool, module_path)

    return export_tools
