# WorkflowRunShape


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** |  | 
**workflow_id** | **str** |  | [optional] 
**workflow_version_id** | **str** |  | 
**workflow_version** | [**WorkflowVersion**](WorkflowVersion.md) |  | [optional] 
**status** | [**WorkflowRunStatus**](WorkflowRunStatus.md) |  | 
**display_name** | **str** |  | [optional] 
**job_runs** | [**List[JobRun]**](JobRun.md) |  | [optional] 
**triggered_by** | [**WorkflowRunTriggeredBy**](WorkflowRunTriggeredBy.md) |  | 
**input** | **Dict[str, object]** |  | [optional] 
**error** | **str** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**duration** | **int** |  | [optional] 
**parent_id** | **str** |  | [optional] 
**parent_step_run_id** | **str** |  | [optional] 
**additional_metadata** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.workflow_run_shape import WorkflowRunShape

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowRunShape from a JSON string
workflow_run_shape_instance = WorkflowRunShape.from_json(json)
# print the JSON string representation of the object
print(WorkflowRunShape.to_json())

# convert the object into a dict
workflow_run_shape_dict = workflow_run_shape_instance.to_dict()
# create an instance of WorkflowRunShape from a dict
workflow_run_shape_from_dict = WorkflowRunShape.from_dict(workflow_run_shape_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


