# TeamConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_turns** | **int** |  | [optional] 
**participants** | **List[object]** |  | [optional] 
**termination_condition** | [**ComponentModel**](ComponentModel.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.team_config import TeamConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TeamConfig from a JSON string
team_config_instance = TeamConfig.from_json(json)
# print the JSON string representation of the object
print(TeamConfig.to_json())

# convert the object into a dict
team_config_dict = team_config_instance.to_dict()
# create an instance of TeamConfig from a dict
team_config_from_dict = TeamConfig.from_dict(team_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


