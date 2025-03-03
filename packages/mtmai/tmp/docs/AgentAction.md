# AgentAction

agent 执行动作

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tool** | **str** | 工具名称 | 
**tool_input** | **str** | 工具输入 | 
**log** | **str** | 工具日志 | 
**tool_id** | **str** | 工具ID | 

## Example

```python
from mtmai.clients.rest.models.agent_action import AgentAction

# TODO update the JSON string below
json = "{}"
# create an instance of AgentAction from a JSON string
agent_action_instance = AgentAction.from_json(json)
# print the JSON string representation of the object
print(AgentAction.to_json())

# convert the object into a dict
agent_action_dict = agent_action_instance.to_dict()
# create an instance of AgentAction from a dict
agent_action_from_dict = AgentAction.from_dict(agent_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


