# FlowTeamInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session_id** | **str** |  | 
**component** | [**TeamComponent**](TeamComponent.md) |  | 
**task** | **str** |  | 
**init_state** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.flow_team_input import FlowTeamInput

# TODO update the JSON string below
json = "{}"
# create an instance of FlowTeamInput from a JSON string
flow_team_input_instance = FlowTeamInput.from_json(json)
# print the JSON string representation of the object
print(FlowTeamInput.to_json())

# convert the object into a dict
flow_team_input_dict = flow_team_input_instance.to_dict()
# create an instance of FlowTeamInput from a dict
flow_team_input_from_dict = FlowTeamInput.from_dict(flow_team_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


