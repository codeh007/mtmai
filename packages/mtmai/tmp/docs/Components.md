# Components


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** |  | [optional] 
**component_type** | **str** |  | [default to 'team']
**version** | **int** |  | [optional] 
**component_version** | **int** |  | [optional] 
**description** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**config** | [**RoundRobinGroupChatConfig**](RoundRobinGroupChatConfig.md) |  | 
**termination_condition** | [**Terminations**](Terminations.md) |  | 

## Example

```python
from mtmai.clients.rest.models.components import Components

# TODO update the JSON string below
json = "{}"
# create an instance of Components from a JSON string
components_instance = Components.from_json(json)
# print the JSON string representation of the object
print(Components.to_json())

# convert the object into a dict
components_dict = components_instance.to_dict()
# create an instance of Components from a dict
components_from_dict = Components.from_dict(components_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


