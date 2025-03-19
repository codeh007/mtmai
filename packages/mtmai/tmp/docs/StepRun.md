# StepRun


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** |  | 
**job_run_id** | **str** |  | 
**job_run** | **Dict[str, object]** |  | [optional] 
**step_id** | **str** |  | 
**step** | [**Step**](Step.md) |  | [optional] 
**child_workflows_count** | **int** |  | [optional] 
**parents** | **List[str]** |  | [optional] 
**child_workflow_runs** | **List[str]** |  | [optional] 
**worker_id** | **str** |  | [optional] 
**input** | **str** |  | [optional] 
**output** | **str** |  | [optional] 
**status** | [**StepRunStatus**](StepRunStatus.md) |  | 
**requeue_after** | **datetime** |  | [optional] 
**result** | **object** |  | [optional] 
**error** | **str** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**started_at_epoch** | **int** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**finished_at_epoch** | **int** |  | [optional] 
**timeout_at** | **datetime** |  | [optional] 
**timeout_at_epoch** | **int** |  | [optional] 
**cancelled_at** | **datetime** |  | [optional] 
**cancelled_at_epoch** | **int** |  | [optional] 
**cancelled_reason** | **str** |  | [optional] 
**cancelled_error** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.step_run import StepRun

# TODO update the JSON string below
json = "{}"
# create an instance of StepRun from a JSON string
step_run_instance = StepRun.from_json(json)
# print the JSON string representation of the object
print(StepRun.to_json())

# convert the object into a dict
step_run_dict = step_run_instance.to_dict()
# create an instance of StepRun from a dict
step_run_from_dict = StepRun.from_dict(step_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


