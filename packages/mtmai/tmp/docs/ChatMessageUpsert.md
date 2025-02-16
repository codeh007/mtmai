# ChatMessageUpsert


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tenant_id** | **str** |  | 
**content** | **str** |  | 
**team_id** | **str** |  | 
**thread_id** | **str** |  | [optional] 
**run_id** | **str** |  | [optional] 
**role** | [**ChatMessageRole**](ChatMessageRole.md) |  | [optional] 
**message_type** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessageUpsert from a JSON string
chat_message_upsert_instance = ChatMessageUpsert.from_json(json)
# print the JSON string representation of the object
print(ChatMessageUpsert.to_json())

# convert the object into a dict
chat_message_upsert_dict = chat_message_upsert_instance.to_dict()
# create an instance of ChatMessageUpsert from a dict
chat_message_upsert_from_dict = ChatMessageUpsert.from_dict(chat_message_upsert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


