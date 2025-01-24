# CancelEventRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_ids** | **List[str]** |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.cancel_event_request import CancelEventRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CancelEventRequest from a JSON string
cancel_event_request_instance = CancelEventRequest.from_json(json)
# print the JSON string representation of the object
print(CancelEventRequest.to_json())

# convert the object into a dict
cancel_event_request_dict = cancel_event_request_instance.to_dict()
# create an instance of CancelEventRequest from a dict
cancel_event_request_from_dict = CancelEventRequest.from_dict(cancel_event_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


