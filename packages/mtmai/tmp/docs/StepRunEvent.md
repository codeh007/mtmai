# StepRunEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**time_first_seen** | **datetime** |  | 
**time_last_seen** | **datetime** |  | 
**step_run_id** | **str** |  | [optional] 
**workflow_run_id** | **str** |  | [optional] 
**reason** | [**StepRunEventReason**](StepRunEventReason.md) |  | 
**severity** | [**StepRunEventSeverity**](StepRunEventSeverity.md) |  | 
**message** | **str** |  | 
**count** | **int** |  | 
**data** | **object** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.step_run_event import StepRunEvent

# TODO update the JSON string below
json = "{}"
# create an instance of StepRunEvent from a JSON string
step_run_event_instance = StepRunEvent.from_json(json)
# print the JSON string representation of the object
print(StepRunEvent.to_json())

# convert the object into a dict
step_run_event_dict = step_run_event_instance.to_dict()
# create an instance of StepRunEvent from a dict
step_run_event_from_dict = StepRunEvent.from_dict(step_run_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


