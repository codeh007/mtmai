# WorkflowConcurrency


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_runs** | **int** | The maximum number of concurrent workflow runs. | 
**limit_strategy** | **str** | The strategy to use when the concurrency limit is reached. | 
**get_concurrency_group** | **str** | An action which gets the concurrency group for the WorkflowRun. | 

## Example

```python
from mtmai.clients.rest.models.workflow_concurrency import WorkflowConcurrency

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowConcurrency from a JSON string
workflow_concurrency_instance = WorkflowConcurrency.from_json(json)
# print the JSON string representation of the object
print(WorkflowConcurrency.to_json())

# convert the object into a dict
workflow_concurrency_dict = workflow_concurrency_instance.to_dict()
# create an instance of WorkflowConcurrency from a dict
workflow_concurrency_from_dict = WorkflowConcurrency.from_dict(workflow_concurrency_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


