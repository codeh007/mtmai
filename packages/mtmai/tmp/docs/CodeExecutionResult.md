# CodeExecutionResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**output** | **str** | The result of the code execution | 
**success** | **bool** | Whether the code execution was successful | 

## Example

```python
from mtmai.clients.rest.models.code_execution_result import CodeExecutionResult

# TODO update the JSON string below
json = "{}"
# create an instance of CodeExecutionResult from a JSON string
code_execution_result_instance = CodeExecutionResult.from_json(json)
# print the JSON string representation of the object
print(CodeExecutionResult.to_json())

# convert the object into a dict
code_execution_result_dict = code_execution_result_instance.to_dict()
# create an instance of CodeExecutionResult from a dict
code_execution_result_from_dict = CodeExecutionResult.from_dict(code_execution_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


