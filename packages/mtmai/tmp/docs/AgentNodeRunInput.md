# AgentNodeRunInput

agent运行节点请求

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**flow_name** | [**FlowNames**](FlowNames.md) |  | 
**node_id** | **str** | agent 节点ID(threadId) | [optional] 
**is_stream** | **bool** | 是否使用stream 传输事件 | [optional] 
**params** | [**AgentNodeRunInputParams**](AgentNodeRunInputParams.md) |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_node_run_input import AgentNodeRunInput

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeRunInput from a JSON string
agent_node_run_input_instance = AgentNodeRunInput.from_json(json)
# print the JSON string representation of the object
print(AgentNodeRunInput.to_json())

# convert the object into a dict
agent_node_run_input_dict = agent_node_run_input_instance.to_dict()
# create an instance of AgentNodeRunInput from a dict
agent_node_run_input_from_dict = AgentNodeRunInput.from_dict(agent_node_run_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


