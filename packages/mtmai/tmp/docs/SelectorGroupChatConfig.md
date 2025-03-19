# SelectorGroupChatConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**participants** | [**List[AgentComponent]**](AgentComponent.md) |  | 
**max_turns** | **int** |  | 
**termination_condition** | [**TextMentionTerminationComponent**](TextMentionTerminationComponent.md) |  | 
**model_client** | [**ModelComponent**](ModelComponent.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.selector_group_chat_config import SelectorGroupChatConfig

# TODO update the JSON string below
json = "{}"
# create an instance of SelectorGroupChatConfig from a JSON string
selector_group_chat_config_instance = SelectorGroupChatConfig.from_json(json)
# print the JSON string representation of the object
print(SelectorGroupChatConfig.to_json())

# convert the object into a dict
selector_group_chat_config_dict = selector_group_chat_config_instance.to_dict()
# create an instance of SelectorGroupChatConfig from a dict
selector_group_chat_config_from_dict = SelectorGroupChatConfig.from_dict(selector_group_chat_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


