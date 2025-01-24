# AgentNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**title** | **str** | agent 节点名称, 或者作为工具名称 | 
**description** | **str** | agent 节点描述, 或者作为工具描述 | 
**type** | **str** | 节点类型，决定了由哪个agent来进行调度 | [optional] 
**config** | **object** | agent 的配置 | [optional] 
**state** | [**AgentState**](AgentState.md) |  | [optional] 
**steps** | [**List[AgentStep]**](AgentStep.md) | agent 节点执行步骤, 一般表示之前执行的步骤 | 
**finish** | [**AgentFinish**](AgentFinish.md) |  | [optional] 
**parent_id** | **str** | 上级节点 | [optional] 
**agent_node_output** | [**AgentNodeOutput**](AgentNodeOutput.md) |  | [optional] 
**tools** | **str** |  | [optional] 
**memory_id** | **str** | 记忆ID，表示这个agent的记忆 | [optional] 
**input** | **str** | 输入 | [optional] 
**output** | **str** | 输出 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_node import AgentNode

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNode from a JSON string
agent_node_instance = AgentNode.from_json(json)
# print the JSON string representation of the object
print(AgentNode.to_json())

# convert the object into a dict
agent_node_dict = agent_node_instance.to_dict()
# create an instance of AgentNode from a dict
agent_node_from_dict = AgentNode.from_dict(agent_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


