# Team


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | 
**provider** | **str** |  | 
**config** | **object** |  | 
**max_turns** | **int** |  | [default to 25]

## Example

```python
from mtmai.clients.rest.models.team import Team

# TODO update the JSON string below
json = "{}"
# create an instance of Team from a JSON string
team_instance = Team.from_json(json)
# print the JSON string representation of the object
print(Team.to_json())

# convert the object into a dict
team_dict = team_instance.to_dict()
# create an instance of Team from a dict
team_from_dict = Team.from_dict(team_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


