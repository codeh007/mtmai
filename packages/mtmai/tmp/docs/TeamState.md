# TeamState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**agent_states** | **object** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.team_state import TeamState

# TODO update the JSON string below
json = "{}"
# create an instance of TeamState from a JSON string
team_state_instance = TeamState.from_json(json)
# print the JSON string representation of the object
print(TeamState.to_json())

# convert the object into a dict
team_state_dict = team_state_instance.to_dict()
# create an instance of TeamState from a dict
team_state_from_dict = TeamState.from_dict(team_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


