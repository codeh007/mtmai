# EventBase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.event_base import EventBase

# TODO update the JSON string below
json = "{}"
# create an instance of EventBase from a JSON string
event_base_instance = EventBase.from_json(json)
# print the JSON string representation of the object
print(EventBase.to_json())

# convert the object into a dict
event_base_dict = event_base_instance.to_dict()
# create an instance of EventBase from a dict
event_base_from_dict = EventBase.from_dict(event_base_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


