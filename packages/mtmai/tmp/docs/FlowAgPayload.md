# FlowAgPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**team_id** | **str** |  | 
**session_id** | **str** |  | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.flow_ag_payload import FlowAgPayload

# TODO update the JSON string below
json = "{}"
# create an instance of FlowAgPayload from a JSON string
flow_ag_payload_instance = FlowAgPayload.from_json(json)
# print the JSON string representation of the object
print(FlowAgPayload.to_json())

# convert the object into a dict
flow_ag_payload_dict = flow_ag_payload_instance.to_dict()
# create an instance of FlowAgPayload from a dict
flow_ag_payload_from_dict = FlowAgPayload.from_dict(flow_ag_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


