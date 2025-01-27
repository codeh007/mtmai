# CallAgent

调用 Agent 参数

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm** | [**LlmConfig**](LlmConfig.md) | 大语言模型 api 配置 | [optional] 
**input** | **object** | 输入参数 | 
**agents** | [**List[CrewAiAgent]**](CrewAiAgent.md) | agents 列表 | 
**tasks** | [**List[CrewAiTask]**](CrewAiTask.md) | 任务列表 | 
**debug** | **bool** | 是否调试模式 | [optional] [default to False]

## Example

```python
from mtmaisdk.clients.rest.models.call_agent import CallAgent

# TODO update the JSON string below
json = "{}"
# create an instance of CallAgent from a JSON string
call_agent_instance = CallAgent.from_json(json)
# print the JSON string representation of the object
print(CallAgent.to_json())

# convert the object into a dict
call_agent_dict = call_agent_instance.to_dict()
# create an instance of CallAgent from a dict
call_agent_from_dict = CallAgent.from_dict(call_agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


