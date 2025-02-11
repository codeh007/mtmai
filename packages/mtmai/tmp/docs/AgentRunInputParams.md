# AgentRunInputParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | 
**input** | **str** |  | [optional] 
**team_id** | **str** |  | 
**session_id** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.agent_run_input_params import AgentRunInputParams

# TODO update the JSON string below
json = "{}"
# create an instance of AgentRunInputParams from a JSON string
agent_run_input_params_instance = AgentRunInputParams.from_json(json)
# print the JSON string representation of the object
print(AgentRunInputParams.to_json())

# convert the object into a dict
agent_run_input_params_dict = agent_run_input_params_instance.to_dict()
# create an instance of AgentRunInputParams from a dict
agent_run_input_params_from_dict = AgentRunInputParams.from_dict(agent_run_input_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


