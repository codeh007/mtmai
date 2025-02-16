# TeamComponent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** | Describes how the component can be instantiated. | 
**component_type** | [**ComponentTypes**](ComponentTypes.md) | Logical type of the component. If missing, the component assumes the default type of the provider. | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | [optional] 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | [optional] 
**description** | **str** | Description of the component. | [optional] 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | [optional] 
**config** | [**TeamConfig**](TeamConfig.md) |  | 

## Example

```python
from mtmai.clients.rest.models.team_component import TeamComponent

# TODO update the JSON string below
json = "{}"
# create an instance of TeamComponent from a JSON string
team_component_instance = TeamComponent.from_json(json)
# print the JSON string representation of the object
print(TeamComponent.to_json())

# convert the object into a dict
team_component_dict = team_component_instance.to_dict()
# create an instance of TeamComponent from a dict
team_component_from_dict = TeamComponent.from_dict(team_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


