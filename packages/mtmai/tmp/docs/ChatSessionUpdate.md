# ChatSessionUpdate

更新聊天 Session

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.chat_session_update import ChatSessionUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSessionUpdate from a JSON string
chat_session_update_instance = ChatSessionUpdate.from_json(json)
# print the JSON string representation of the object
print(ChatSessionUpdate.to_json())

# convert the object into a dict
chat_session_update_dict = chat_session_update_instance.to_dict()
# create an instance of ChatSessionUpdate from a dict
chat_session_update_from_dict = ChatSessionUpdate.from_dict(chat_session_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


