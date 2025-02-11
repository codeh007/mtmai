# StopMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.stop_message_config import StopMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of StopMessageConfig from a JSON string
stop_message_config_instance = StopMessageConfig.from_json(json)
# print the JSON string representation of the object
print(StopMessageConfig.to_json())

# convert the object into a dict
stop_message_config_dict = stop_message_config_instance.to_dict()
# create an instance of StopMessageConfig from a dict
stop_message_config_from_dict = StopMessageConfig.from_dict(stop_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


