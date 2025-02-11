# StepRunEventList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[StepRunEvent]**](StepRunEvent.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.step_run_event_list import StepRunEventList

# TODO update the JSON string below
json = "{}"
# create an instance of StepRunEventList from a JSON string
step_run_event_list_instance = StepRunEventList.from_json(json)
# print the JSON string representation of the object
print(StepRunEventList.to_json())

# convert the object into a dict
step_run_event_list_dict = step_run_event_list_instance.to_dict()
# create an instance of StepRunEventList from a dict
step_run_event_list_from_dict = StepRunEventList.from_dict(step_run_event_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


