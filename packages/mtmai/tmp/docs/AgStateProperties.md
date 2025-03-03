# AgStateProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** |  | [optional] [default to '1.0.0']
**type** | **str** |  | [optional] [default to 'TeamState']
**component_id** | **str** | 组件id | [optional] 
**chat_id** | **str** | 聊天id | [optional] 
**state** | **Dict[str, object]** |  | 

## Example

```python
from mtmai.clients.rest.models.ag_state_properties import AgStateProperties

# TODO update the JSON string below
json = "{}"
# create an instance of AgStateProperties from a JSON string
ag_state_properties_instance = AgStateProperties.from_json(json)
# print the JSON string representation of the object
print(AgStateProperties.to_json())

# convert the object into a dict
ag_state_properties_dict = ag_state_properties_instance.to_dict()
# create an instance of AgStateProperties from a dict
ag_state_properties_from_dict = AgStateProperties.from_dict(ag_state_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


