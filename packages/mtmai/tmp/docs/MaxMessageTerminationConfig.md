# MaxMessageTerminationConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**termination_type** | **str** |  | 
**max_messages** | **int** |  | 

## Example

```python
from mtmai.clients.rest.models.max_message_termination_config import MaxMessageTerminationConfig

# TODO update the JSON string below
json = "{}"
# create an instance of MaxMessageTerminationConfig from a JSON string
max_message_termination_config_instance = MaxMessageTerminationConfig.from_json(json)
# print the JSON string representation of the object
print(MaxMessageTerminationConfig.to_json())

# convert the object into a dict
max_message_termination_config_dict = max_message_termination_config_instance.to_dict()
# create an instance of MaxMessageTerminationConfig from a dict
max_message_termination_config_from_dict = MaxMessageTerminationConfig.from_dict(max_message_termination_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


