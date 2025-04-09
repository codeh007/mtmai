# AskUserFunctionCallInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] [default to 'AskUserFunctionCallInput']
**title** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.ask_user_function_call_input import AskUserFunctionCallInput

# TODO update the JSON string below
json = "{}"
# create an instance of AskUserFunctionCallInput from a JSON string
ask_user_function_call_input_instance = AskUserFunctionCallInput.from_json(json)
# print the JSON string representation of the object
print(AskUserFunctionCallInput.to_json())

# convert the object into a dict
ask_user_function_call_input_dict = ask_user_function_call_input_instance.to_dict()
# create an instance of AskUserFunctionCallInput from a dict
ask_user_function_call_input_from_dict = AskUserFunctionCallInput.from_dict(ask_user_function_call_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


