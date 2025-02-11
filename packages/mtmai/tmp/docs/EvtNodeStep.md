# EvtNodeStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | 节点名称 | 
**input** | **str** | 节点输入 | 

## Example

```python
from mtmaisdk.clients.rest.models.evt_node_step import EvtNodeStep

# TODO update the JSON string below
json = "{}"
# create an instance of EvtNodeStep from a JSON string
evt_node_step_instance = EvtNodeStep.from_json(json)
# print the JSON string representation of the object
print(EvtNodeStep.to_json())

# convert the object into a dict
evt_node_step_dict = evt_node_step_instance.to_dict()
# create an instance of EvtNodeStep from a dict
evt_node_step_from_dict = EvtNodeStep.from_dict(evt_node_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


