# MultiModalMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | [**List[MultiModalMessageConfigAllOfContent]**](MultiModalMessageConfigAllOfContent.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.multi_modal_message_config import MultiModalMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of MultiModalMessageConfig from a JSON string
multi_modal_message_config_instance = MultiModalMessageConfig.from_json(json)
# print the JSON string representation of the object
print(MultiModalMessageConfig.to_json())

# convert the object into a dict
multi_modal_message_config_dict = multi_modal_message_config_instance.to_dict()
# create an instance of MultiModalMessageConfig from a dict
multi_modal_message_config_from_dict = MultiModalMessageConfig.from_dict(multi_modal_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


