# AssistantAgentConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**model_context** | **Dict[str, object]** |  | [optional] 
**memory** | **Dict[str, object]** |  | [optional] 
**model_client_stream** | **bool** |  | [optional] [default to False]
**system_message** | **str** |  | [optional] 
**model_client** | [**MtOpenAIChatCompletionClientComponent**](MtOpenAIChatCompletionClientComponent.md) |  | 
**tools** | **List[Dict[str, object]]** |  | [optional] [default to []]
**handoffs** | **List[str]** |  | [optional] [default to []]
**reflect_on_tool_use** | **bool** |  | [optional] [default to False]
**tool_call_summary_format** | **str** |  | [optional] [default to '{result}']

## Example

```python
from mtmai.clients.rest.models.assistant_agent_config import AssistantAgentConfig

# TODO update the JSON string below
json = "{}"
# create an instance of AssistantAgentConfig from a JSON string
assistant_agent_config_instance = AssistantAgentConfig.from_json(json)
# print the JSON string representation of the object
print(AssistantAgentConfig.to_json())

# convert the object into a dict
assistant_agent_config_dict = assistant_agent_config_instance.to_dict()
# create an instance of AssistantAgentConfig from a dict
assistant_agent_config_from_dict = AssistantAgentConfig.from_dict(assistant_agent_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


