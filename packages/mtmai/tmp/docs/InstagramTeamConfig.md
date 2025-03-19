# InstagramTeamConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**participants** | [**List[InstagramTeamConfigAllOfParticipants]**](InstagramTeamConfigAllOfParticipants.md) |  | 
**max_turns** | **int** |  | 
**termination_condition** | [**OrTerminationComponent**](OrTerminationComponent.md) |  | 

## Example

```python
from mtmai.clients.rest.models.instagram_team_config import InstagramTeamConfig

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramTeamConfig from a JSON string
instagram_team_config_instance = InstagramTeamConfig.from_json(json)
# print the JSON string representation of the object
print(InstagramTeamConfig.to_json())

# convert the object into a dict
instagram_team_config_dict = instagram_team_config_instance.to_dict()
# create an instance of InstagramTeamConfig from a dict
instagram_team_config_from_dict = InstagramTeamConfig.from_dict(instagram_team_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


