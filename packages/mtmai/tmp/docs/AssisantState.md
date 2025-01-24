# AssisantState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**thread_id** | **str** | 线程ID | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | 
**name** | **str** | 名称 | 
**description** | **str** | 描述 | 

## Example

```python
from mtmai.gomtmclients.rest.models.assisant_state import AssisantState

# TODO update the JSON string below
json = "{}"
# create an instance of AssisantState from a JSON string
assisant_state_instance = AssisantState.from_json(json)
# print the JSON string representation of the object
print(AssisantState.to_json())

# convert the object into a dict
assisant_state_dict = assisant_state_instance.to_dict()
# create an instance of AssisantState from a dict
assisant_state_from_dict = AssisantState.from_dict(assisant_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


