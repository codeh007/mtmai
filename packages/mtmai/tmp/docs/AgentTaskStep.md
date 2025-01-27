# AgentTaskStep

任务执行步骤

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | 工具名称 | 
**create_at** | **str** | 步骤启动时间 | 
**input_type** | **str** | 步骤输入类型(human,ai,tool) | [optional] 
**input** | **str** | 步骤输入 | 
**output** | **str** | 步骤输出 | 
**is_final** | **bool** | 是否是最终步骤 | [optional] 
**reason** | **str** | 步骤执行原因 | 

## Example

```python
from mtmaisdk.clients.rest.models.agent_task_step import AgentTaskStep

# TODO update the JSON string below
json = "{}"
# create an instance of AgentTaskStep from a JSON string
agent_task_step_instance = AgentTaskStep.from_json(json)
# print the JSON string representation of the object
print(AgentTaskStep.to_json())

# convert the object into a dict
agent_task_step_dict = agent_task_step_instance.to_dict()
# create an instance of AgentTaskStep from a dict
agent_task_step_from_dict = AgentTaskStep.from_dict(agent_task_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


