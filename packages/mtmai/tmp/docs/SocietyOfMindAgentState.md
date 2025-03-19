# SocietyOfMindAgentState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**inner_team_state** | **object** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.society_of_mind_agent_state import SocietyOfMindAgentState

# TODO update the JSON string below
json = "{}"
# create an instance of SocietyOfMindAgentState from a JSON string
society_of_mind_agent_state_instance = SocietyOfMindAgentState.from_json(json)
# print the JSON string representation of the object
print(SocietyOfMindAgentState.to_json())

# convert the object into a dict
society_of_mind_agent_state_dict = society_of_mind_agent_state_instance.to_dict()
# create an instance of SocietyOfMindAgentState from a dict
society_of_mind_agent_state_from_dict = SocietyOfMindAgentState.from_dict(society_of_mind_agent_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


