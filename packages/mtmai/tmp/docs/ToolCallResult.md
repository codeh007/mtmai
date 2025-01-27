# ToolCallResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | 结果id | [optional] 
**data** | **str** | 结果数据 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.tool_call_result import ToolCallResult

# TODO update the JSON string below
json = "{}"
# create an instance of ToolCallResult from a JSON string
tool_call_result_instance = ToolCallResult.from_json(json)
# print the JSON string representation of the object
print(ToolCallResult.to_json())

# convert the object into a dict
tool_call_result_dict = tool_call_result_instance.to_dict()
# create an instance of ToolCallResult from a dict
tool_call_result_from_dict = ToolCallResult.from_dict(tool_call_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


