# FlowStateProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session_id** | **str** |  | 
**state** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.flow_state_properties import FlowStateProperties

# TODO update the JSON string below
json = "{}"
# create an instance of FlowStateProperties from a JSON string
flow_state_properties_instance = FlowStateProperties.from_json(json)
# print the JSON string representation of the object
print(FlowStateProperties.to_json())

# convert the object into a dict
flow_state_properties_dict = flow_state_properties_instance.to_dict()
# create an instance of FlowStateProperties from a dict
flow_state_properties_from_dict = FlowStateProperties.from_dict(flow_state_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


