# ChatUpsert


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
from mtmai.clients.rest.models.chat_upsert import ChatUpsert

# TODO update the JSON string below
json = "{}"
# create an instance of ChatUpsert from a JSON string
chat_upsert_instance = ChatUpsert.from_json(json)
# print the JSON string representation of the object
print(ChatUpsert.to_json())

# convert the object into a dict
chat_upsert_dict = chat_upsert_instance.to_dict()
# create an instance of ChatUpsert from a dict
chat_upsert_from_dict = ChatUpsert.from_dict(chat_upsert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


