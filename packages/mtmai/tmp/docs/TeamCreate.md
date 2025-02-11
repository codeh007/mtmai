# TeamCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**version** | **int** |  | [optional] 
**team_type** | [**TeamTypes**](TeamTypes.md) |  | [optional] 
**component** | [**TeamComponent**](TeamComponent.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.team_create import TeamCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TeamCreate from a JSON string
team_create_instance = TeamCreate.from_json(json)
# print the JSON string representation of the object
print(TeamCreate.to_json())

# convert the object into a dict
team_create_dict = team_create_instance.to_dict()
# create an instance of TeamCreate from a dict
team_create_from_dict = TeamCreate.from_dict(team_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


