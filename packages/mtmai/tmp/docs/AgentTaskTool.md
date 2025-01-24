# AgentTaskTool

agent 任务工具

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | 工具名称 | 
**description** | **str** | 工具描述 | 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_task_tool import AgentTaskTool

# TODO update the JSON string below
json = "{}"
# create an instance of AgentTaskTool from a JSON string
agent_task_tool_instance = AgentTaskTool.from_json(json)
# print the JSON string representation of the object
print(AgentTaskTool.to_json())

# convert the object into a dict
agent_task_tool_dict = agent_task_tool_instance.to_dict()
# create an instance of AgentTaskTool from a dict
agent_task_tool_from_dict = AgentTaskTool.from_dict(agent_task_tool_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


