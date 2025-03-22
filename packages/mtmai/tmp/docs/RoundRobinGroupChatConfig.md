# RoundRobinGroupChatConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**participants** | [**List[AgentComponent]**](AgentComponent.md) |  | 
**max_turns** | **int** |  | 
**termination_condition** | [**TextMentionTerminationComponent**](TextMentionTerminationComponent.md) |  | 

## Example

```python
from mtmai.clients.rest.models.round_robin_group_chat_config import RoundRobinGroupChatConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RoundRobinGroupChatConfig from a JSON string
round_robin_group_chat_config_instance = RoundRobinGroupChatConfig.from_json(json)
# print the JSON string representation of the object
print(RoundRobinGroupChatConfig.to_json())

# convert the object into a dict
round_robin_group_chat_config_dict = round_robin_group_chat_config_instance.to_dict()
# create an instance of RoundRobinGroupChatConfig from a dict
round_robin_group_chat_config_from_dict = RoundRobinGroupChatConfig.from_dict(round_robin_group_chat_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


