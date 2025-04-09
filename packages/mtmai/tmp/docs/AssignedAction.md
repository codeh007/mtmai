# AssignedAction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tenant_id** | **str** |  | 
**workflow_run_id** | **str** |  | [optional] 
**get_group_key_run_id** | **str** |  | [optional] 
**job_id** | **str** |  | 
**job_name** | **str** |  | [optional] 
**step_id** | **str** |  | 
**step_run_id** | **str** |  | [optional] 
**action_id** | **str** |  | 
**action_type** | **str** |  | 
**action_payload** | **str** |  | 
**step_name** | **str** |  | 
**retry_count** | **int** |  | 
**additional_metadata** | **str** |  | [optional] 
**child_workflow_index** | **int** |  | [optional] 
**child_workflow_key** | **str** |  | [optional] 
**parent_workflow_run_id** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.assigned_action import AssignedAction

# TODO update the JSON string below
json = "{}"
# create an instance of AssignedAction from a JSON string
assigned_action_instance = AssignedAction.from_json(json)
# print the JSON string representation of the object
print(AssignedAction.to_json())

# convert the object into a dict
assigned_action_dict = assigned_action_instance.to_dict()
# create an instance of AssignedAction from a dict
assigned_action_from_dict = AssignedAction.from_dict(assigned_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


