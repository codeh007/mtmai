# RecentStepRuns


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**action_id** | **str** | The action id. | 
**status** | [**StepRunStatus**](StepRunStatus.md) |  | 
**started_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**cancelled_at** | **datetime** |  | [optional] 
**workflow_run_id** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.recent_step_runs import RecentStepRuns

# TODO update the JSON string below
json = "{}"
# create an instance of RecentStepRuns from a JSON string
recent_step_runs_instance = RecentStepRuns.from_json(json)
# print the JSON string representation of the object
print(RecentStepRuns.to_json())

# convert the object into a dict
recent_step_runs_dict = recent_step_runs_instance.to_dict()
# create an instance of RecentStepRuns from a dict
recent_step_runs_from_dict = RecentStepRuns.from_dict(recent_step_runs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


