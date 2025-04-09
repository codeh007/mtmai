# FlowResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [default to 'FlowLoginResult']
**success** | **bool** |  | [optional] 
**source** | **str** |  | [optional] 
**account_id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.flow_result import FlowResult

# TODO update the JSON string below
json = "{}"
# create an instance of FlowResult from a JSON string
flow_result_instance = FlowResult.from_json(json)
# print the JSON string representation of the object
print(FlowResult.to_json())

# convert the object into a dict
flow_result_dict = flow_result_instance.to_dict()
# create an instance of FlowResult from a dict
flow_result_from_dict = FlowResult.from_dict(flow_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


