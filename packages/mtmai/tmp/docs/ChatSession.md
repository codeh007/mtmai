# ChatSession

聊天 Session

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**name** | **str** |  | 
**version** | **str** |  | 
**team** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.chat_session import ChatSession

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSession from a JSON string
chat_session_instance = ChatSession.from_json(json)
# print the JSON string representation of the object
print(ChatSession.to_json())

# convert the object into a dict
chat_session_dict = chat_session_instance.to_dict()
# create an instance of ChatSession from a dict
chat_session_from_dict = ChatSession.from_dict(chat_session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


