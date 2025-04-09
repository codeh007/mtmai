# AssistantAgentState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**llm_context** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.assistant_agent_state import AssistantAgentState

# TODO update the JSON string below
json = "{}"
# create an instance of AssistantAgentState from a JSON string
assistant_agent_state_instance = AssistantAgentState.from_json(json)
# print the JSON string representation of the object
print(AssistantAgentState.to_json())

# convert the object into a dict
assistant_agent_state_dict = assistant_agent_state_instance.to_dict()
# create an instance of AssistantAgentState from a dict
assistant_agent_state_from_dict = AssistantAgentState.from_dict(assistant_agent_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


