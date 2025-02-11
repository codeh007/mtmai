# StartWorkflowRunEvent

用户调用工作流后, 后端返回工作流启动状态的事件, 一般用于根据 Id,从 stream api 中进一步拉取更加详细的事件

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**workflow_run_id** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.start_workflow_run_event import StartWorkflowRunEvent

# TODO update the JSON string below
json = "{}"
# create an instance of StartWorkflowRunEvent from a JSON string
start_workflow_run_event_instance = StartWorkflowRunEvent.from_json(json)
# print the JSON string representation of the object
print(StartWorkflowRunEvent.to_json())

# convert the object into a dict
start_workflow_run_event_dict = start_workflow_run_event_instance.to_dict()
# create an instance of StartWorkflowRunEvent from a dict
start_workflow_run_event_from_dict = StartWorkflowRunEvent.from_dict(start_workflow_run_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


