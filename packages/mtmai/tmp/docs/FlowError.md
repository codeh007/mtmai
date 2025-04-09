# FlowError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**error** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.flow_error import FlowError

# TODO update the JSON string below
json = "{}"
# create an instance of FlowError from a JSON string
flow_error_instance = FlowError.from_json(json)
# print the JSON string representation of the object
print(FlowError.to_json())

# convert the object into a dict
flow_error_dict = flow_error_instance.to_dict()
# create an instance of FlowError from a dict
flow_error_from_dict = FlowError.from_dict(flow_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


