# Event


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**key** | **str** | The key for the event. | 
**tenant** | [**Tenant**](Tenant.md) | The tenant associated with this event. | [optional] 
**tenant_id** | **str** | The ID of the tenant associated with this event. | 
**workflow_run_summary** | [**EventWorkflowRunSummary**](EventWorkflowRunSummary.md) | The workflow run summary for this event. | [optional] 
**additional_metadata** | **object** | Additional metadata for the event. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.event import Event

# TODO update the JSON string below
json = "{}"
# create an instance of Event from a JSON string
event_instance = Event.from_json(json)
# print the JSON string representation of the object
print(Event.to_json())

# convert the object into a dict
event_dict = event_instance.to_dict()
# create an instance of Event from a dict
event_from_dict = Event.from_dict(event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


