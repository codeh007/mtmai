# WorkflowRunsMetricsCounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pending** | **int** |  | [optional] 
**running** | **int** |  | [optional] 
**succeeded** | **int** |  | [optional] 
**failed** | **int** |  | [optional] 
**queued** | **int** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.workflow_runs_metrics_counts import WorkflowRunsMetricsCounts

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowRunsMetricsCounts from a JSON string
workflow_runs_metrics_counts_instance = WorkflowRunsMetricsCounts.from_json(json)
# print the JSON string representation of the object
print(WorkflowRunsMetricsCounts.to_json())

# convert the object into a dict
workflow_runs_metrics_counts_dict = workflow_runs_metrics_counts_instance.to_dict()
# create an instance of WorkflowRunsMetricsCounts from a dict
workflow_runs_metrics_counts_from_dict = WorkflowRunsMetricsCounts.from_dict(workflow_runs_metrics_counts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


