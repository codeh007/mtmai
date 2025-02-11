# TeamList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Team]**](Team.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.team_list import TeamList

# TODO update the JSON string below
json = "{}"
# create an instance of TeamList from a JSON string
team_list_instance = TeamList.from_json(json)
# print the JSON string representation of the object
print(TeamList.to_json())

# convert the object into a dict
team_list_dict = team_list_instance.to_dict()
# create an instance of TeamList from a dict
team_list_from_dict = TeamList.from_dict(team_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


