# ReplayEventRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_ids** | **List[str]** |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.replay_event_request import ReplayEventRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplayEventRequest from a JSON string
replay_event_request_instance = ReplayEventRequest.from_json(json)
# print the JSON string representation of the object
print(ReplayEventRequest.to_json())

# convert the object into a dict
replay_event_request_dict = replay_event_request_instance.to_dict()
# create an instance of ReplayEventRequest from a dict
replay_event_request_from_dict = ReplayEventRequest.from_dict(replay_event_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


