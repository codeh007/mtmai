# AgentNodeOutput

agent 节点输出

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**is_final** | **bool** | 是否是最终步骤 | 
**more_steps** | [**List[AgentStep]**](AgentStep.md) | 更多步骤 | 
**output** | **object** | 输出 | 
**error** | **str** | 错误 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_node_output import AgentNodeOutput

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeOutput from a JSON string
agent_node_output_instance = AgentNodeOutput.from_json(json)
# print the JSON string representation of the object
print(AgentNodeOutput.to_json())

# convert the object into a dict
agent_node_output_dict = agent_node_output_instance.to_dict()
# create an instance of AgentNodeOutput from a dict
agent_node_output_from_dict = AgentNodeOutput.from_dict(agent_node_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


