# ChatMessageList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**rows** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_message_list import ChatMessageList

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessageList from a JSON string
chat_message_list_instance = ChatMessageList.from_json(json)
# print the JSON string representation of the object
print(ChatMessageList.to_json())

# convert the object into a dict
chat_message_list_dict = chat_message_list_instance.to_dict()
# create an instance of ChatMessageList from a dict
chat_message_list_from_dict = ChatMessageList.from_dict(chat_message_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


