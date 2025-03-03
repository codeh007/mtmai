# AgentNodeCreateRequest

创建agent节点请求

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | agent 节点名称, 或者作为工具名称 | [optional] 
**prompt** | **str** | agent 节点提示词 | 
**description** | **str** | agent 节点描述, 或者作为工具描述 | [optional] 

## Example

```python
from mtmai.clients.rest.models.agent_node_create_request import AgentNodeCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeCreateRequest from a JSON string
agent_node_create_request_instance = AgentNodeCreateRequest.from_json(json)
# print the JSON string representation of the object
print(AgentNodeCreateRequest.to_json())

# convert the object into a dict
agent_node_create_request_dict = agent_node_create_request_instance.to_dict()
# create an instance of AgentNodeCreateRequest from a dict
agent_node_create_request_from_dict = AgentNodeCreateRequest.from_dict(agent_node_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


