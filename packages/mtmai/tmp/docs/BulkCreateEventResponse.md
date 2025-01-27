# BulkCreateEventResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**events** | [**List[Event]**](Event.md) | The events. | 

## Example

```python
from mtmaisdk.clients.rest.models.bulk_create_event_response import BulkCreateEventResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BulkCreateEventResponse from a JSON string
bulk_create_event_response_instance = BulkCreateEventResponse.from_json(json)
# print the JSON string representation of the object
print(BulkCreateEventResponse.to_json())

# convert the object into a dict
bulk_create_event_response_dict = bulk_create_event_response_instance.to_dict()
# create an instance of BulkCreateEventResponse from a dict
bulk_create_event_response_from_dict = BulkCreateEventResponse.from_dict(bulk_create_event_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


