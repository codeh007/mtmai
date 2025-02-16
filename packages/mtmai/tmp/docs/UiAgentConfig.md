# UiAgentConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**some_value** | **str** | 一些值 | [optional] 

## Example

```python
from mtmai.clients.rest.models.ui_agent_config import UiAgentConfig

# TODO update the JSON string below
json = "{}"
# create an instance of UiAgentConfig from a JSON string
ui_agent_config_instance = UiAgentConfig.from_json(json)
# print the JSON string representation of the object
print(UiAgentConfig.to_json())

# convert the object into a dict
ui_agent_config_dict = ui_agent_config_instance.to_dict()
# create an instance of UiAgentConfig from a dict
ui_agent_config_from_dict = UiAgentConfig.from_dict(ui_agent_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


