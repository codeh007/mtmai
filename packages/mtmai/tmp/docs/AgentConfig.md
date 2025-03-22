# AgentConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**model_context** | **Dict[str, object]** |  | [optional] 
**memory** | [**MemoryConfig**](MemoryConfig.md) |  | [optional] 
**model_client_stream** | **bool** |  | [default to False]
**system_message** | **str** |  | [optional] 
**model_client** | [**ModelComponent**](ModelComponent.md) |  | 
**tools** | [**List[ToolComponent]**](ToolComponent.md) |  | [default to []]
**handoffs** | **List[str]** |  | [default to []]
**reflect_on_tool_use** | **bool** |  | [default to False]
**tool_call_summary_format** | **str** |  | [default to '{result}']

## Example

```python
from mtmai.clients.rest.models.agent_config import AgentConfig

# TODO update the JSON string below
json = "{}"
# create an instance of AgentConfig from a JSON string
agent_config_instance = AgentConfig.from_json(json)
# print the JSON string representation of the object
print(AgentConfig.to_json())

# convert the object into a dict
agent_config_dict = agent_config_instance.to_dict()
# create an instance of AgentConfig from a dict
agent_config_from_dict = AgentConfig.from_dict(agent_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


