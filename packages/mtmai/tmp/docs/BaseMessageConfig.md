# BaseMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.base_message_config import BaseMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of BaseMessageConfig from a JSON string
base_message_config_instance = BaseMessageConfig.from_json(json)
# print the JSON string representation of the object
print(BaseMessageConfig.to_json())

# convert the object into a dict
base_message_config_dict = base_message_config_instance.to_dict()
# create an instance of BaseMessageConfig from a dict
base_message_config_from_dict = BaseMessageConfig.from_dict(base_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


