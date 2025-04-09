# AskUserFunctionCallInputFieldValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**value** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.ask_user_function_call_input_field_value import AskUserFunctionCallInputFieldValue

# TODO update the JSON string below
json = "{}"
# create an instance of AskUserFunctionCallInputFieldValue from a JSON string
ask_user_function_call_input_field_value_instance = AskUserFunctionCallInputFieldValue.from_json(json)
# print the JSON string representation of the object
print(AskUserFunctionCallInputFieldValue.to_json())

# convert the object into a dict
ask_user_function_call_input_field_value_dict = ask_user_function_call_input_field_value_instance.to_dict()
# create an instance of AskUserFunctionCallInputFieldValue from a dict
ask_user_function_call_input_field_value_from_dict = AskUserFunctionCallInputFieldValue.from_dict(ask_user_function_call_input_field_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


