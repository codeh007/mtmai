# FlowStateUpsert


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session_id** | **str** |  | 
**state** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.flow_state_upsert import FlowStateUpsert

# TODO update the JSON string below
json = "{}"
# create an instance of FlowStateUpsert from a JSON string
flow_state_upsert_instance = FlowStateUpsert.from_json(json)
# print the JSON string representation of the object
print(FlowStateUpsert.to_json())

# convert the object into a dict
flow_state_upsert_dict = flow_state_upsert_instance.to_dict()
# create an instance of FlowStateUpsert from a dict
flow_state_upsert_from_dict = FlowStateUpsert.from_dict(flow_state_upsert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


