# UiAgentState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**welcome** | [**ChatWelcome**](ChatWelcome.md) |  | [optional] 
**thread_id** | **str** | 线程ID(sessionId) | [optional] 
**team_id** | **str** | 当前选定的 team id | [optional] 

## Example

```python
from mtmai.clients.rest.models.ui_agent_state import UiAgentState

# TODO update the JSON string below
json = "{}"
# create an instance of UiAgentState from a JSON string
ui_agent_state_instance = UiAgentState.from_json(json)
# print the JSON string representation of the object
print(UiAgentState.to_json())

# convert the object into a dict
ui_agent_state_dict = ui_agent_state_instance.to_dict()
# create an instance of UiAgentState from a dict
ui_agent_state_from_dict = UiAgentState.from_dict(ui_agent_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


