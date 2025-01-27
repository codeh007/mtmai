# ChatHistoryList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.chat_history_list import ChatHistoryList

# TODO update the JSON string below
json = "{}"
# create an instance of ChatHistoryList from a JSON string
chat_history_list_instance = ChatHistoryList.from_json(json)
# print the JSON string representation of the object
print(ChatHistoryList.to_json())

# convert the object into a dict
chat_history_list_dict = chat_history_list_instance.to_dict()
# create an instance of ChatHistoryList from a dict
chat_history_list_from_dict = ChatHistoryList.from_dict(chat_history_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


