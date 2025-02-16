# TeamResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task_result** | **object** |  | 
**usage** | **str** |  | 
**duration** | **float** |  | 

## Example

```python
from mtmai.clients.rest.models.team_result import TeamResult

# TODO update the JSON string below
json = "{}"
# create an instance of TeamResult from a JSON string
team_result_instance = TeamResult.from_json(json)
# print the JSON string representation of the object
print(TeamResult.to_json())

# convert the object into a dict
team_result_dict = team_result_instance.to_dict()
# create an instance of TeamResult from a dict
team_result_from_dict = TeamResult.from_dict(team_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


