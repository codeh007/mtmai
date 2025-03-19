# HandoffConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.handoff_config import HandoffConfig

# TODO update the JSON string below
json = "{}"
# create an instance of HandoffConfig from a JSON string
handoff_config_instance = HandoffConfig.from_json(json)
# print the JSON string representation of the object
print(HandoffConfig.to_json())

# convert the object into a dict
handoff_config_dict = handoff_config_instance.to_dict()
# create an instance of HandoffConfig from a dict
handoff_config_from_dict = HandoffConfig.from_dict(handoff_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


