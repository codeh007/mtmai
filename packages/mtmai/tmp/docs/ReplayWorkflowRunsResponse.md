# ReplayWorkflowRunsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_runs** | [**List[WorkflowRun]**](WorkflowRun.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.replay_workflow_runs_response import ReplayWorkflowRunsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayWorkflowRunsResponse from a JSON string
replay_workflow_runs_response_instance = ReplayWorkflowRunsResponse.from_json(json)
# print the JSON string representation of the object
print(ReplayWorkflowRunsResponse.to_json())

# convert the object into a dict
replay_workflow_runs_response_dict = replay_workflow_runs_response_instance.to_dict()
# create an instance of ReplayWorkflowRunsResponse from a dict
replay_workflow_runs_response_from_dict = ReplayWorkflowRunsResponse.from_dict(replay_workflow_runs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


