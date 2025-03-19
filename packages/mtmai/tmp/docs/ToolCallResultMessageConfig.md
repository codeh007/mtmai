# ToolCallResultMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | [**List[FunctionExecutionResult]**](FunctionExecutionResult.md) |  | 

## Example

```python
from mtmai.clients.rest.models.tool_call_result_message_config import ToolCallResultMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of ToolCallResultMessageConfig from a JSON string
tool_call_result_message_config_instance = ToolCallResultMessageConfig.from_json(json)
# print the JSON string representation of the object
print(ToolCallResultMessageConfig.to_json())

# convert the object into a dict
tool_call_result_message_config_dict = tool_call_result_message_config_instance.to_dict()
# create an instance of ToolCallResultMessageConfig from a dict
tool_call_result_message_config_from_dict = ToolCallResultMessageConfig.from_dict(tool_call_result_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


