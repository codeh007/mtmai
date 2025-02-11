# FunctionExecutionResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**call_id** | **str** |  | 
**content** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.function_execution_result import FunctionExecutionResult

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionExecutionResult from a JSON string
function_execution_result_instance = FunctionExecutionResult.from_json(json)
# print the JSON string representation of the object
print(FunctionExecutionResult.to_json())

# convert the object into a dict
function_execution_result_dict = function_execution_result_instance.to_dict()
# create an instance of FunctionExecutionResult from a dict
function_execution_result_from_dict = FunctionExecutionResult.from_dict(function_execution_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


