# WorkflowRunsCancelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_run_ids** | **List[str]** |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.workflow_runs_cancel_request import WorkflowRunsCancelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowRunsCancelRequest from a JSON string
workflow_runs_cancel_request_instance = WorkflowRunsCancelRequest.from_json(json)
# print the JSON string representation of the object
print(WorkflowRunsCancelRequest.to_json())

# convert the object into a dict
workflow_runs_cancel_request_dict = workflow_runs_cancel_request_instance.to_dict()
# create an instance of WorkflowRunsCancelRequest from a dict
workflow_runs_cancel_request_from_dict = WorkflowRunsCancelRequest.from_dict(workflow_runs_cancel_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


