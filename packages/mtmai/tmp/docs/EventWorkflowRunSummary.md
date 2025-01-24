# EventWorkflowRunSummary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pending** | **int** | The number of pending runs. | [optional] 
**running** | **int** | The number of running runs. | [optional] 
**queued** | **int** | The number of queued runs. | [optional] 
**succeeded** | **int** | The number of succeeded runs. | [optional] 
**failed** | **int** | The number of failed runs. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.event_workflow_run_summary import EventWorkflowRunSummary

# TODO update the JSON string below
json = "{}"
# create an instance of EventWorkflowRunSummary from a JSON string
event_workflow_run_summary_instance = EventWorkflowRunSummary.from_json(json)
# print the JSON string representation of the object
print(EventWorkflowRunSummary.to_json())

# convert the object into a dict
event_workflow_run_summary_dict = event_workflow_run_summary_instance.to_dict()
# create an instance of EventWorkflowRunSummary from a dict
event_workflow_run_summary_from_dict = EventWorkflowRunSummary.from_dict(event_workflow_run_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


