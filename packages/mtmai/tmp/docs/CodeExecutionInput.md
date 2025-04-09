# CodeExecutionInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The contents of the Python code block that should be executed | 

## Example

```python
from mtmai.clients.rest.models.code_execution_input import CodeExecutionInput

# TODO update the JSON string below
json = "{}"
# create an instance of CodeExecutionInput from a JSON string
code_execution_input_instance = CodeExecutionInput.from_json(json)
# print the JSON string representation of the object
print(CodeExecutionInput.to_json())

# convert the object into a dict
code_execution_input_dict = code_execution_input_instance.to_dict()
# create an instance of CodeExecutionInput from a dict
code_execution_input_from_dict = CodeExecutionInput.from_dict(code_execution_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


