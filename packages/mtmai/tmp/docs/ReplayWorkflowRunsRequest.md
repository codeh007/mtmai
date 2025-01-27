# ReplayWorkflowRunsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_run_ids** | **List[str]** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.replay_workflow_runs_request import ReplayWorkflowRunsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayWorkflowRunsRequest from a JSON string
replay_workflow_runs_request_instance = ReplayWorkflowRunsRequest.from_json(json)
# print the JSON string representation of the object
print(ReplayWorkflowRunsRequest.to_json())

# convert the object into a dict
replay_workflow_runs_request_dict = replay_workflow_runs_request_instance.to_dict()
# create an instance of ReplayWorkflowRunsRequest from a dict
replay_workflow_runs_request_from_dict = ReplayWorkflowRunsRequest.from_dict(replay_workflow_runs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


