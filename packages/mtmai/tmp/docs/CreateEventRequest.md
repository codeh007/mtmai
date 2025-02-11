# CreateEventRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The key for the event. | 
**data** | **object** | The data for the event. | 
**additional_metadata** | **object** | Additional metadata for the event. | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.create_event_request import CreateEventRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEventRequest from a JSON string
create_event_request_instance = CreateEventRequest.from_json(json)
# print the JSON string representation of the object
print(CreateEventRequest.to_json())

# convert the object into a dict
create_event_request_dict = create_event_request_instance.to_dict()
# create an instance of CreateEventRequest from a dict
create_event_request_from_dict = CreateEventRequest.from_dict(create_event_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


