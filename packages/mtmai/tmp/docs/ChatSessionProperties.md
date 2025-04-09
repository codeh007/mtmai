# ChatSessionProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**title** | **str** |  | 
**name** | **str** |  | 
**state** | **Dict[str, object]** |  | 
**state_type** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.chat_session_properties import ChatSessionProperties

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSessionProperties from a JSON string
chat_session_properties_instance = ChatSessionProperties.from_json(json)
# print the JSON string representation of the object
print(ChatSessionProperties.to_json())

# convert the object into a dict
chat_session_properties_dict = chat_session_properties_instance.to_dict()
# create an instance of ChatSessionProperties from a dict
chat_session_properties_from_dict = ChatSessionProperties.from_dict(chat_session_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


