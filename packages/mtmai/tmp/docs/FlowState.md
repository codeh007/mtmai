# FlowState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**session_id** | **str** |  | 
**state** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.flow_state import FlowState

# TODO update the JSON string below
json = "{}"
# create an instance of FlowState from a JSON string
flow_state_instance = FlowState.from_json(json)
# print the JSON string representation of the object
print(FlowState.to_json())

# convert the object into a dict
flow_state_dict = flow_state_instance.to_dict()
# create an instance of FlowState from a dict
flow_state_from_dict = FlowState.from_dict(flow_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


