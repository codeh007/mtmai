# AgentStep

agent 执行步骤

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**action** | [**AgentAction**](AgentAction.md) |  | 
**observation** | **str** | 步骤观察 | 

## Example

```python
from mtmaisdk.clients.rest.models.agent_step import AgentStep

# TODO update the JSON string below
json = "{}"
# create an instance of AgentStep from a JSON string
agent_step_instance = AgentStep.from_json(json)
# print the JSON string representation of the object
print(AgentStep.to_json())

# convert the object into a dict
agent_step_dict = agent_step_instance.to_dict()
# create an instance of AgentStep from a dict
agent_step_from_dict = AgentStep.from_dict(agent_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


