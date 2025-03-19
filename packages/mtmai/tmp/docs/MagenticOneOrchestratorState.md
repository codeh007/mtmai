# MagenticOneOrchestratorState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**task** | **str** |  | [optional] 
**facts** | **str** |  | [optional] 
**plan** | **str** |  | [optional] 
**n_rounds** | **int** |  | [optional] 
**n_stalls** | **int** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.magentic_one_orchestrator_state import MagenticOneOrchestratorState

# TODO update the JSON string below
json = "{}"
# create an instance of MagenticOneOrchestratorState from a JSON string
magentic_one_orchestrator_state_instance = MagenticOneOrchestratorState.from_json(json)
# print the JSON string representation of the object
print(MagenticOneOrchestratorState.to_json())

# convert the object into a dict
magentic_one_orchestrator_state_dict = magentic_one_orchestrator_state_instance.to_dict()
# create an instance of MagenticOneOrchestratorState from a dict
magentic_one_orchestrator_state_from_dict = MagenticOneOrchestratorState.from_dict(magentic_one_orchestrator_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


