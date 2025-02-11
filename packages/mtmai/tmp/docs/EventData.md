# EventData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **str** | The data for the event (JSON bytes). | 

## Example

```python
from mtmaisdk.clients.rest.models.event_data import EventData

# TODO update the JSON string below
json = "{}"
# create an instance of EventData from a JSON string
event_data_instance = EventData.from_json(json)
# print the JSON string representation of the object
print(EventData.to_json())

# convert the object into a dict
event_data_dict = event_data_instance.to_dict()
# create an instance of EventData from a dict
event_data_from_dict = EventData.from_dict(event_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


