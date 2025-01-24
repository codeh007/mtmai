# ChatReq


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**thread_id** | **str** |  | [optional] 
**profile** | **str** |  | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | 
**params** | **object** | 附加的表单数据 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.chat_req import ChatReq

# TODO update the JSON string below
json = "{}"
# create an instance of ChatReq from a JSON string
chat_req_instance = ChatReq.from_json(json)
# print the JSON string representation of the object
print(ChatReq.to_json())

# convert the object into a dict
chat_req_dict = chat_req_instance.to_dict()
# create an instance of ChatReq from a dict
chat_req_from_dict = ChatReq.from_dict(chat_req_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


