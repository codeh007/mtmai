# SemaphoreSlots


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**step_run_id** | **str** | The step run id. | 
**action_id** | **str** | The action id. | 
**started_at** | **datetime** | The time this slot was started. | [optional] 
**timeout_at** | **datetime** | The time this slot will timeout. | [optional] 
**workflow_run_id** | **str** | The workflow run id. | 
**status** | [**StepRunStatus**](StepRunStatus.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.semaphore_slots import SemaphoreSlots

# TODO update the JSON string below
json = "{}"
# create an instance of SemaphoreSlots from a JSON string
semaphore_slots_instance = SemaphoreSlots.from_json(json)
# print the JSON string representation of the object
print(SemaphoreSlots.to_json())

# convert the object into a dict
semaphore_slots_dict = semaphore_slots_instance.to_dict()
# create an instance of SemaphoreSlots from a dict
semaphore_slots_from_dict = SemaphoreSlots.from_dict(semaphore_slots_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


