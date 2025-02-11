# AgEventTypes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**user_id** | **str** |  | [optional] 
**data** | **object** |  | 
**framework** | **str** |  | 
**step_run_id** | **str** |  | 
**meta** | **Dict[str, object]** |  | [optional] 
**state_id** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.ag_event_types import AgEventTypes

# TODO update the JSON string below
json = "{}"
# create an instance of AgEventTypes from a JSON string
ag_event_types_instance = AgEventTypes.from_json(json)
# print the JSON string representation of the object
print(AgEventTypes.to_json())

# convert the object into a dict
ag_event_types_dict = ag_event_types_instance.to_dict()
# create an instance of AgEventTypes from a dict
ag_event_types_from_dict = AgEventTypes.from_dict(ag_event_types_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


