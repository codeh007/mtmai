# SelectorGroupChatConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** | Describes how the component can be instantiated. | 
**component_type** | [**ComponentTypes**](ComponentTypes.md) | Logical type of the component. If missing, the component assumes the default type of the provider. | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | [optional] 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | [optional] 
**description** | **str** | Description of the component. | [optional] 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | [optional] 
**config** | **object** |  | 
**team_type** | **str** |  | [optional] 
**selector_prompt** | **str** |  | [optional] 
**model_client** | [**ModelConfig**](ModelConfig.md) |  | [optional] 

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


