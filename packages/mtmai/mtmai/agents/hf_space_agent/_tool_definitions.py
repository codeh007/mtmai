from autogen_core.tools import ParametersSchema, ToolSchema


# 例子(没实际功能)
TOOL_OPEN_PATH = ToolSchema(
    name="open_path",
    description="Open a local file or directory at a path in the text-based file browser and return current viewport content.",
    parameters=ParametersSchema(
        type="object",
        properties={
            "path": {
                "type": "string",
                "description": "The relative or absolute path of a local file to visit.",
            },
        },
        required=["path"],
    ),
)