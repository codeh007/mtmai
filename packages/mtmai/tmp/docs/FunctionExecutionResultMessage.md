# FunctionExecutionResultMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**content** | [**List[FunctionExecutionResult]**](FunctionExecutionResult.md) |  | 

## Example

```python
from mtmai.clients.rest.models.function_execution_result_message import FunctionExecutionResultMessage

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionExecutionResultMessage from a JSON string
function_execution_result_message_instance = FunctionExecutionResultMessage.from_json(json)
# print the JSON string representation of the object
print(FunctionExecutionResultMessage.to_json())

# convert the object into a dict
function_execution_result_message_dict = function_execution_result_message_instance.to_dict()
# create an instance of FunctionExecutionResultMessage from a dict
function_execution_result_message_from_dict = FunctionExecutionResultMessage.from_dict(function_execution_result_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


