# ToolCallMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | [**List[FunctionCall]**](FunctionCall.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.tool_call_message_config import ToolCallMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of ToolCallMessageConfig from a JSON string
tool_call_message_config_instance = ToolCallMessageConfig.from_json(json)
# print the JSON string representation of the object
print(ToolCallMessageConfig.to_json())

# convert the object into a dict
tool_call_message_config_dict = tool_call_message_config_instance.to_dict()
# create an instance of ToolCallMessageConfig from a dict
tool_call_message_config_from_dict = ToolCallMessageConfig.from_dict(tool_call_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


