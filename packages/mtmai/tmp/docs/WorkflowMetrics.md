# WorkflowMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_key_runs_count** | **int** | The number of runs for a specific group key (passed via filter) | [optional] 
**group_key_count** | **int** | The total number of concurrency group keys. | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.workflow_metrics import WorkflowMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowMetrics from a JSON string
workflow_metrics_instance = WorkflowMetrics.from_json(json)
# print the JSON string representation of the object
print(WorkflowMetrics.to_json())

# convert the object into a dict
workflow_metrics_dict = workflow_metrics_instance.to_dict()
# create an instance of WorkflowMetrics from a dict
workflow_metrics_from_dict = WorkflowMetrics.from_dict(workflow_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


