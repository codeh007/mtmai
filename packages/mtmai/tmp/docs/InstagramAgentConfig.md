# InstagramAgentConfig


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
from mtmai.clients.rest.models.instagram_agent_config import InstagramAgentConfig

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramAgentConfig from a JSON string
instagram_agent_config_instance = InstagramAgentConfig.from_json(json)
# print the JSON string representation of the object
print(InstagramAgentConfig.to_json())

# convert the object into a dict
instagram_agent_config_dict = instagram_agent_config_instance.to_dict()
# create an instance of InstagramAgentConfig from a dict
instagram_agent_config_from_dict = InstagramAgentConfig.from_dict(instagram_agent_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


