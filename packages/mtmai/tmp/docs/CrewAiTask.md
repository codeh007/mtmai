# CrewAiTask

任务定义

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | 任务描述 | 
**expected_output** | **str** | 期待输出 | 
**output_json_schema_name** | **str** | 任务输出json格式名称 | [optional] 
**agent** | **str** | agent | 

## Example

```python
from mtmai.gomtmclients.rest.models.crew_ai_task import CrewAiTask

# TODO update the JSON string below
json = "{}"
# create an instance of CrewAiTask from a JSON string
crew_ai_task_instance = CrewAiTask.from_json(json)
# print the JSON string representation of the object
print(CrewAiTask.to_json())

# convert the object into a dict
crew_ai_task_dict = crew_ai_task_instance.to_dict()
# create an instance of CrewAiTask from a dict
crew_ai_task_from_dict = CrewAiTask.from_dict(crew_ai_task_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


