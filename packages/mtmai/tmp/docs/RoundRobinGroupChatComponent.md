# RoundRobinGroupChatComponent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the component. | [optional] 
**provider** | **str** |  | 
**component_type** | [**ComponentTypes**](ComponentTypes.md) | Logical type of the component. If missing, the component assumes the default type of the provider. | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | 
**description** | **str** | Description of the component. | 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | 
**config** | [**RoundRobinGroupChatConfig**](RoundRobinGroupChatConfig.md) |  | 

## Example

```python
from mtmai.clients.rest.models.round_robin_group_chat_component import RoundRobinGroupChatComponent

# TODO update the JSON string below
json = "{}"
# create an instance of RoundRobinGroupChatComponent from a JSON string
round_robin_group_chat_component_instance = RoundRobinGroupChatComponent.from_json(json)
# print the JSON string representation of the object
print(RoundRobinGroupChatComponent.to_json())

# convert the object into a dict
round_robin_group_chat_component_dict = round_robin_group_chat_component_instance.to_dict()
# create an instance of RoundRobinGroupChatComponent from a dict
round_robin_group_chat_component_from_dict = RoundRobinGroupChatComponent.from_dict(round_robin_group_chat_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


