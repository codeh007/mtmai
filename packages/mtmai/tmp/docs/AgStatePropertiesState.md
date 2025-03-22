# AgStatePropertiesState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**llm_context** | **object** |  | [optional] 
**agent_states** | **object** |  | [optional] 
**message_thread** | [**List[AgentEvent]**](AgentEvent.md) |  | [optional] 
**current_turn** | **int** |  | [optional] 
**next_speaker_index** | **int** |  | [optional] 
**previous_speaker** | **str** |  | [optional] 
**current_speaker** | **str** |  | [optional] 
**task** | **str** |  | [optional] 
**facts** | **str** |  | [optional] 
**plan** | **str** |  | [optional] 
**n_rounds** | **int** |  | [optional] 
**n_stalls** | **int** |  | [optional] 
**inner_team_state** | **object** |  | [optional] 
**agent_state** | **object** |  | [optional] 
**message_buffer** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.ag_state_properties_state import AgStatePropertiesState

# TODO update the JSON string below
json = "{}"
# create an instance of AgStatePropertiesState from a JSON string
ag_state_properties_state_instance = AgStatePropertiesState.from_json(json)
# print the JSON string representation of the object
print(AgStatePropertiesState.to_json())

# convert the object into a dict
ag_state_properties_state_dict = ag_state_properties_state_instance.to_dict()
# create an instance of AgStatePropertiesState from a dict
ag_state_properties_state_from_dict = AgStatePropertiesState.from_dict(ag_state_properties_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


