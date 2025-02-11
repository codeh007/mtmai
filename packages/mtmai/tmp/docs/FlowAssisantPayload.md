# FlowAssisantPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.flow_assisant_payload import FlowAssisantPayload

# TODO update the JSON string below
json = "{}"
# create an instance of FlowAssisantPayload from a JSON string
flow_assisant_payload_instance = FlowAssisantPayload.from_json(json)
# print the JSON string representation of the object
print(FlowAssisantPayload.to_json())

# convert the object into a dict
flow_assisant_payload_dict = flow_assisant_payload_instance.to_dict()
# create an instance of FlowAssisantPayload from a dict
flow_assisant_payload_from_dict = FlowAssisantPayload.from_dict(flow_assisant_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


