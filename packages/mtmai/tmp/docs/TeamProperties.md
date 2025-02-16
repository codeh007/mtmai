# TeamProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**component_type** | [**TeamTypes**](TeamTypes.md) |  | [optional] 
**version** | **int** |  | [optional] [default to 1]
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**component** | [**TeamComponent**](TeamComponent.md) |  | 

## Example

```python
from mtmai.clients.rest.models.team_properties import TeamProperties

# TODO update the JSON string below
json = "{}"
# create an instance of TeamProperties from a JSON string
team_properties_instance = TeamProperties.from_json(json)
# print the JSON string representation of the object
print(TeamProperties.to_json())

# convert the object into a dict
team_properties_dict = team_properties_instance.to_dict()
# create an instance of TeamProperties from a dict
team_properties_from_dict = TeamProperties.from_dict(team_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


