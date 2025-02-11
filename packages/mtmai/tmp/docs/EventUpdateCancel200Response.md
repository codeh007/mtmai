# EventUpdateCancel200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_run_ids** | **List[str]** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.event_update_cancel200_response import EventUpdateCancel200Response

# TODO update the JSON string below
json = "{}"
# create an instance of EventUpdateCancel200Response from a JSON string
event_update_cancel200_response_instance = EventUpdateCancel200Response.from_json(json)
# print the JSON string representation of the object
print(EventUpdateCancel200Response.to_json())

# convert the object into a dict
event_update_cancel200_response_dict = event_update_cancel200_response_instance.to_dict()
# create an instance of EventUpdateCancel200Response from a dict
event_update_cancel200_response_from_dict = EventUpdateCancel200Response.from_dict(event_update_cancel200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


