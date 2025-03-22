# TriggerWorkflowRunRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input** | **object** |  | 
**additional_metadata** | **object** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.trigger_workflow_run_request import TriggerWorkflowRunRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TriggerWorkflowRunRequest from a JSON string
trigger_workflow_run_request_instance = TriggerWorkflowRunRequest.from_json(json)
# print the JSON string representation of the object
print(TriggerWorkflowRunRequest.to_json())

# convert the object into a dict
trigger_workflow_run_request_dict = trigger_workflow_run_request_instance.to_dict()
# create an instance of TriggerWorkflowRunRequest from a dict
trigger_workflow_run_request_from_dict = TriggerWorkflowRunRequest.from_dict(trigger_workflow_run_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


