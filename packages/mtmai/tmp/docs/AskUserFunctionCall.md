# AskUserFunctionCall


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] [default to 'AskUserFunctionCall']
**id** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**fields** | [**List[FormField]**](FormField.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.ask_user_function_call import AskUserFunctionCall

# TODO update the JSON string below
json = "{}"
# create an instance of AskUserFunctionCall from a JSON string
ask_user_function_call_instance = AskUserFunctionCall.from_json(json)
# print the JSON string representation of the object
print(AskUserFunctionCall.to_json())

# convert the object into a dict
ask_user_function_call_dict = ask_user_function_call_instance.to_dict()
# create an instance of AskUserFunctionCall from a dict
ask_user_function_call_from_dict = AskUserFunctionCall.from_dict(ask_user_function_call_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


