# TerminationConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**termination_type** | [**TerminationTypes**](TerminationTypes.md) |  | [optional] 
**conditions** | [**List[TerminationConditions]**](TerminationConditions.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.termination_config import TerminationConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TerminationConfig from a JSON string
termination_config_instance = TerminationConfig.from_json(json)
# print the JSON string representation of the object
print(TerminationConfig.to_json())

# convert the object into a dict
termination_config_dict = termination_config_instance.to_dict()
# create an instance of TerminationConfig from a dict
termination_config_from_dict = TerminationConfig.from_dict(termination_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


