# ChatSessionList

聊天 Session 列表

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[ChatSession]**](ChatSession.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_session_list import ChatSessionList

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSessionList from a JSON string
chat_session_list_instance = ChatSessionList.from_json(json)
# print the JSON string representation of the object
print(ChatSessionList.to_json())

# convert the object into a dict
chat_session_list_dict = chat_session_list_instance.to_dict()
# create an instance of ChatSessionList from a dict
chat_session_list_from_dict = ChatSessionList.from_dict(chat_session_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


