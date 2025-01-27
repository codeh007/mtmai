# AgentNodeInput

agent 节点输入

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**inputs** | **object** | 输入 | 
**intermediate_steps** | [**List[AgentStep]**](AgentStep.md) | 中间步骤 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.agent_node_input import AgentNodeInput

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeInput from a JSON string
agent_node_input_instance = AgentNodeInput.from_json(json)
# print the JSON string representation of the object
print(AgentNodeInput.to_json())

# convert the object into a dict
agent_node_input_dict = agent_node_input_instance.to_dict()
# create an instance of AgentNodeInput from a dict
agent_node_input_from_dict = AgentNodeInput.from_dict(agent_node_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


