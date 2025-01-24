# BaseState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**thread_id** | **str** | 线程ID | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | 

## Example

```python
from mtmai.gomtmclients.rest.models.base_state import BaseState

# TODO update the JSON string below
json = "{}"
# create an instance of BaseState from a JSON string
base_state_instance = BaseState.from_json(json)
# print the JSON string representation of the object
print(BaseState.to_json())

# convert the object into a dict
base_state_dict = base_state_instance.to_dict()
# create an instance of BaseState from a dict
base_state_from_dict = BaseState.from_dict(base_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


