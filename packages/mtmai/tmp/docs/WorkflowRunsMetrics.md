# WorkflowRunsMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**counts** | [**WorkflowRunsMetricsCounts**](.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.workflow_runs_metrics import WorkflowRunsMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowRunsMetrics from a JSON string
workflow_runs_metrics_instance = WorkflowRunsMetrics.from_json(json)
# print the JSON string representation of the object
print(WorkflowRunsMetrics.to_json())

# convert the object into a dict
workflow_runs_metrics_dict = workflow_runs_metrics_instance.to_dict()
# create an instance of WorkflowRunsMetrics from a dict
workflow_runs_metrics_from_dict = WorkflowRunsMetrics.from_dict(workflow_runs_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


