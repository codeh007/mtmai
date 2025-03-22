# SwarmManagerState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**current_speaker** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.swarm_manager_state import SwarmManagerState

# TODO update the JSON string below
json = "{}"
# create an instance of SwarmManagerState from a JSON string
swarm_manager_state_instance = SwarmManagerState.from_json(json)
# print the JSON string representation of the object
print(SwarmManagerState.to_json())

# convert the object into a dict
swarm_manager_state_dict = swarm_manager_state_instance.to_dict()
# create an instance of SwarmManagerState from a dict
swarm_manager_state_from_dict = SwarmManagerState.from_dict(swarm_manager_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


