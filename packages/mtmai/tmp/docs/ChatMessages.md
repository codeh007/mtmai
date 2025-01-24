# ChatMessages

聊天消息列表

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.chat_messages import ChatMessages

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessages from a JSON string
chat_messages_instance = ChatMessages.from_json(json)
# print the JSON string representation of the object
print(ChatMessages.to_json())

# convert the object into a dict
chat_messages_dict = chat_messages_instance.to_dict()
# create an instance of ChatMessages from a dict
chat_messages_from_dict = ChatMessages.from_dict(chat_messages_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


