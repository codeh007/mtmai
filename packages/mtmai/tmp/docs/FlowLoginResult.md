# FlowLoginResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [default to 'FlowLoginResult']
**success** | **bool** |  | [optional] 
**source** | **str** |  | [optional] 
**account_id** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.flow_login_result import FlowLoginResult

# TODO update the JSON string below
json = "{}"
# create an instance of FlowLoginResult from a JSON string
flow_login_result_instance = FlowLoginResult.from_json(json)
# print the JSON string representation of the object
print(FlowLoginResult.to_json())

# convert the object into a dict
flow_login_result_dict = flow_login_result_instance.to_dict()
# create an instance of FlowLoginResult from a dict
flow_login_result_from_dict = FlowLoginResult.from_dict(flow_login_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


