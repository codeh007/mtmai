# AgEventUpdate


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
from mtmaisdk.clients.rest.models.ag_event_update import AgEventUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of AgEventUpdate from a JSON string
ag_event_update_instance = AgEventUpdate.from_json(json)
# print the JSON string representation of the object
print(AgEventUpdate.to_json())

# convert the object into a dict
ag_event_update_dict = ag_event_update_instance.to_dict()
# create an instance of AgEventUpdate from a dict
ag_event_update_from_dict = AgEventUpdate.from_dict(ag_event_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


