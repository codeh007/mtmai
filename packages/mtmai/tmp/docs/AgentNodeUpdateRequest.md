# AgentNodeUpdateRequest

创建agent节点请求

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | agent 节点名称, 或者作为工具名称 | [optional] 
**prompt** | **str** | agent 节点提示词 | 
**type** | **str** | agent 节点类型 | [optional] 
**description** | **str** | agent 节点描述 | [optional] 
**state** | **object** | agent 节点状态 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_node_update_request import AgentNodeUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeUpdateRequest from a JSON string
agent_node_update_request_instance = AgentNodeUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(AgentNodeUpdateRequest.to_json())

# convert the object into a dict
agent_node_update_request_dict = agent_node_update_request_instance.to_dict()
# create an instance of AgentNodeUpdateRequest from a dict
agent_node_update_request_from_dict = AgentNodeUpdateRequest.from_dict(agent_node_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


