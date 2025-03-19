# ChatSessionStartEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**thread_id** | **str** |  | [optional] 
**source** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_session_start_event import ChatSessionStartEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSessionStartEvent from a JSON string
chat_session_start_event_instance = ChatSessionStartEvent.from_json(json)
# print the JSON string representation of the object
print(ChatSessionStartEvent.to_json())

# convert the object into a dict
chat_session_start_event_dict = chat_session_start_event_instance.to_dict()
# create an instance of ChatSessionStartEvent from a dict
chat_session_start_event_from_dict = ChatSessionStartEvent.from_dict(chat_session_start_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


