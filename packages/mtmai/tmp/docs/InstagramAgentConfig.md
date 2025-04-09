# InstagramAgentConfig


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
**username** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**otp_key** | **str** |  | [optional] 
**proxy_url** | **str** |  | [optional] 

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


