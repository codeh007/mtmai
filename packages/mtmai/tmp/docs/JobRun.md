# JobRun


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** |  | 
**workflow_run_id** | **str** |  | 
**workflow_run** | [**WorkflowRun**](WorkflowRun.md) |  | [optional] 
**job_id** | **str** |  | 
**job** | [**Job**](Job.md) |  | [optional] 
**ticker_id** | **str** |  | [optional] 
**step_runs** | [**List[StepRun]**](StepRun.md) |  | [optional] 
**status** | [**JobRunStatus**](JobRunStatus.md) |  | 
**result** | **object** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**timeout_at** | **datetime** |  | [optional] 
**cancelled_at** | **datetime** |  | [optional] 
**cancelled_reason** | **str** |  | [optional] 
**cancelled_error** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.job_run import JobRun

# TODO update the JSON string below
json = "{}"
# create an instance of JobRun from a JSON string
job_run_instance = JobRun.from_json(json)
# print the JSON string representation of the object
print(JobRun.to_json())

# convert the object into a dict
job_run_dict = job_run_instance.to_dict()
# create an instance of JobRun from a dict
job_run_from_dict = JobRun.from_dict(job_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


