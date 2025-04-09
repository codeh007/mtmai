# FlowHandoffResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**success** | **bool** |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.flow_handoff_result import FlowHandoffResult

# TODO update the JSON string below
json = "{}"
# create an instance of FlowHandoffResult from a JSON string
flow_handoff_result_instance = FlowHandoffResult.from_json(json)
# print the JSON string representation of the object
print(FlowHandoffResult.to_json())

# convert the object into a dict
flow_handoff_result_dict = flow_handoff_result_instance.to_dict()
# create an instance of FlowHandoffResult from a dict
flow_handoff_result_from_dict = FlowHandoffResult.from_dict(flow_handoff_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


