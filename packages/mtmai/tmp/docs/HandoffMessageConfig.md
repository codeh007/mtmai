# HandoffMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | **str** |  | 
**target** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.handoff_message_config import HandoffMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of HandoffMessageConfig from a JSON string
handoff_message_config_instance = HandoffMessageConfig.from_json(json)
# print the JSON string representation of the object
print(HandoffMessageConfig.to_json())

# convert the object into a dict
handoff_message_config_dict = handoff_message_config_instance.to_dict()
# create an instance of HandoffMessageConfig from a dict
handoff_message_config_from_dict = HandoffMessageConfig.from_dict(handoff_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


