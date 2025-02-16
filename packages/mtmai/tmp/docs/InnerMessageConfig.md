# InnerMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | [**List[FunctionExecutionResult]**](FunctionExecutionResult.md) |  | 

## Example

```python
from mtmai.clients.rest.models.inner_message_config import InnerMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of InnerMessageConfig from a JSON string
inner_message_config_instance = InnerMessageConfig.from_json(json)
# print the JSON string representation of the object
print(InnerMessageConfig.to_json())

# convert the object into a dict
inner_message_config_dict = inner_message_config_instance.to_dict()
# create an instance of InnerMessageConfig from a dict
inner_message_config_from_dict = InnerMessageConfig.from_dict(inner_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


