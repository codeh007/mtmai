# ChatMessagePropertiesConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message_type** | **str** |  | [optional] 
**source** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_message_properties_config import ChatMessagePropertiesConfig

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessagePropertiesConfig from a JSON string
chat_message_properties_config_instance = ChatMessagePropertiesConfig.from_json(json)
# print the JSON string representation of the object
print(ChatMessagePropertiesConfig.to_json())

# convert the object into a dict
chat_message_properties_config_dict = chat_message_properties_config_instance.to_dict()
# create an instance of ChatMessagePropertiesConfig from a dict
chat_message_properties_config_from_dict = ChatMessagePropertiesConfig.from_dict(chat_message_properties_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


