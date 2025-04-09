# ChatMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**type** | [**MtLlmMessageTypes**](MtLlmMessageTypes.md) |  | 
**content** | **str** |  | 
**llm_message** | [**MtLlmMessage**](MtLlmMessage.md) |  | 
**content_type** | **str** |  | 
**source** | **str** |  | 
**topic** | **str** |  | 
**thread_id** | **str** |  | 
**config** | [**ChatMessagePropertiesConfig**](ChatMessagePropertiesConfig.md) |  | [optional] 
**model_usage** | [**ModelUsage**](ModelUsage.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_message import ChatMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessage from a JSON string
chat_message_instance = ChatMessage.from_json(json)
# print the JSON string representation of the object
print(ChatMessage.to_json())

# convert the object into a dict
chat_message_dict = chat_message_instance.to_dict()
# create an instance of ChatMessage from a dict
chat_message_from_dict = ChatMessage.from_dict(chat_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


