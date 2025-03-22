# RoundRobinManagerState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**message_thread** | [**List[AgentEvent]**](AgentEvent.md) |  | [optional] 
**current_turn** | **int** |  | [optional] 
**next_speaker_index** | **int** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.round_robin_manager_state import RoundRobinManagerState

# TODO update the JSON string below
json = "{}"
# create an instance of RoundRobinManagerState from a JSON string
round_robin_manager_state_instance = RoundRobinManagerState.from_json(json)
# print the JSON string representation of the object
print(RoundRobinManagerState.to_json())

# convert the object into a dict
round_robin_manager_state_dict = round_robin_manager_state_instance.to_dict()
# create an instance of RoundRobinManagerState from a dict
round_robin_manager_state_from_dict = RoundRobinManagerState.from_dict(round_robin_manager_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


