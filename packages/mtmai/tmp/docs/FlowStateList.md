# FlowStateList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[FlowState]**](FlowState.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.flow_state_list import FlowStateList

# TODO update the JSON string below
json = "{}"
# create an instance of FlowStateList from a JSON string
flow_state_list_instance = FlowStateList.from_json(json)
# print the JSON string representation of the object
print(FlowStateList.to_json())

# convert the object into a dict
flow_state_list_dict = flow_state_list_instance.to_dict()
# create an instance of FlowStateList from a dict
flow_state_list_from_dict = FlowStateList.from_dict(flow_state_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


