# AgEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**user_id** | **str** |  | [optional] 
**data** | **object** |  | 
**framework** | **str** |  | 
**step_run_id** | **str** |  | 
**meta** | **object** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.ag_event import AgEvent

# TODO update the JSON string below
json = "{}"
# create an instance of AgEvent from a JSON string
ag_event_instance = AgEvent.from_json(json)
# print the JSON string representation of the object
print(AgEvent.to_json())

# convert the object into a dict
ag_event_dict = ag_event_instance.to_dict()
# create an instance of AgEvent from a dict
ag_event_from_dict = AgEvent.from_dict(ag_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


