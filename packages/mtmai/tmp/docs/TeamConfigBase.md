# TeamConfigBase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**participants** | [**List[AgentComponent]**](AgentComponent.md) |  | 
**max_turns** | **int** |  | 
**termination_condition** | [**TextMentionTerminationComponent**](TextMentionTerminationComponent.md) |  | 

## Example

```python
from mtmai.clients.rest.models.team_config_base import TeamConfigBase

# TODO update the JSON string below
json = "{}"
# create an instance of TeamConfigBase from a JSON string
team_config_base_instance = TeamConfigBase.from_json(json)
# print the JSON string representation of the object
print(TeamConfigBase.to_json())

# convert the object into a dict
team_config_base_dict = team_config_base_instance.to_dict()
# create an instance of TeamConfigBase from a dict
team_config_base_from_dict = TeamConfigBase.from_dict(team_config_base_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


