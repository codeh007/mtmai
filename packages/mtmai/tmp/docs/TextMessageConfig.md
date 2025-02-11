# TextMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.text_message_config import TextMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TextMessageConfig from a JSON string
text_message_config_instance = TextMessageConfig.from_json(json)
# print the JSON string representation of the object
print(TextMessageConfig.to_json())

# convert the object into a dict
text_message_config_dict = text_message_config_instance.to_dict()
# create an instance of TextMessageConfig from a dict
text_message_config_from_dict = TextMessageConfig.from_dict(text_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


