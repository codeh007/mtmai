# AgentNodeRun

agentnode run

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**state** | **object** |  | [optional] 
**workflow_run_id** | **str** |  | 
**node_id** | **str** |  | 
**input** | **object** |  | [optional] 
**output** | **object** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_node_run import AgentNodeRun

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeRun from a JSON string
agent_node_run_instance = AgentNodeRun.from_json(json)
# print the JSON string representation of the object
print(AgentNodeRun.to_json())

# convert the object into a dict
agent_node_run_dict = agent_node_run_instance.to_dict()
# create an instance of AgentNodeRun from a dict
agent_node_run_from_dict = AgentNodeRun.from_dict(agent_node_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


