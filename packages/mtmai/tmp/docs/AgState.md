# AgState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**version** | **str** |  | [optional] [default to '1.0.0']
**type** | **str** |  | [optional] [default to 'TeamState']
**component_id** | **str** | 组件id | [optional] 
**chat_id** | **str** | 聊天id | [optional] 
**state** | **Dict[str, object]** |  | 

## Example

```python
from mtmai.clients.rest.models.ag_state import AgState

# TODO update the JSON string below
json = "{}"
# create an instance of AgState from a JSON string
ag_state_instance = AgState.from_json(json)
# print the JSON string representation of the object
print(AgState.to_json())

# convert the object into a dict
ag_state_dict = ag_state_instance.to_dict()
# create an instance of AgState from a dict
ag_state_from_dict = AgState.from_dict(ag_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


