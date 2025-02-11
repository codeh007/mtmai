# BulkCreateEventRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[CreateEventRequest]**](CreateEventRequest.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.bulk_create_event_request import BulkCreateEventRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BulkCreateEventRequest from a JSON string
bulk_create_event_request_instance = BulkCreateEventRequest.from_json(json)
# print the JSON string representation of the object
print(BulkCreateEventRequest.to_json())

# convert the object into a dict
bulk_create_event_request_dict = bulk_create_event_request_instance.to_dict()
# create an instance of BulkCreateEventRequest from a dict
bulk_create_event_request_from_dict = BulkCreateEventRequest.from_dict(bulk_create_event_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


