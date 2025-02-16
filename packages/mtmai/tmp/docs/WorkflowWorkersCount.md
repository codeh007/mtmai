# WorkflowWorkersCount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**free_slot_count** | **int** |  | [optional] 
**max_slot_count** | **int** |  | [optional] 
**workflow_run_id** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.workflow_workers_count import WorkflowWorkersCount

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowWorkersCount from a JSON string
workflow_workers_count_instance = WorkflowWorkersCount.from_json(json)
# print the JSON string representation of the object
print(WorkflowWorkersCount.to_json())

# convert the object into a dict
workflow_workers_count_dict = workflow_workers_count_instance.to_dict()
# create an instance of WorkflowWorkersCount from a dict
workflow_workers_count_from_dict = WorkflowWorkersCount.from_dict(workflow_workers_count_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


