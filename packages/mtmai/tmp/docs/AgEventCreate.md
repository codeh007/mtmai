# AgEventCreate


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
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate

# TODO update the JSON string below
json = "{}"
# create an instance of AgEventCreate from a JSON string
ag_event_create_instance = AgEventCreate.from_json(json)
# print the JSON string representation of the object
print(AgEventCreate.to_json())

# convert the object into a dict
ag_event_create_dict = ag_event_create_instance.to_dict()
# create an instance of AgEventCreate from a dict
ag_event_create_from_dict = AgEventCreate.from_dict(ag_event_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


