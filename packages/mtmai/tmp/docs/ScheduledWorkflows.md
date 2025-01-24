# ScheduledWorkflows


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** |  | 
**workflow_version_id** | **str** |  | 
**workflow_id** | **str** |  | 
**workflow_name** | **str** |  | 
**trigger_at** | **datetime** |  | 
**input** | **Dict[str, object]** |  | [optional] 
**additional_metadata** | **Dict[str, object]** |  | [optional] 
**workflow_run_created_at** | **datetime** |  | [optional] 
**workflow_run_name** | **str** |  | [optional] 
**workflow_run_status** | [**WorkflowRunStatus**](WorkflowRunStatus.md) |  | [optional] 
**workflow_run_id** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.scheduled_workflows import ScheduledWorkflows

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduledWorkflows from a JSON string
scheduled_workflows_instance = ScheduledWorkflows.from_json(json)
# print the JSON string representation of the object
print(ScheduledWorkflows.to_json())

# convert the object into a dict
scheduled_workflows_dict = scheduled_workflows_instance.to_dict()
# create an instance of ScheduledWorkflows from a dict
scheduled_workflows_from_dict = ScheduledWorkflows.from_dict(scheduled_workflows_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


