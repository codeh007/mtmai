# AgStateProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** |  | [optional] [default to '1.0.0']
**type** | [**StateType**](StateType.md) |  | 
**component_id** | **str** |  | [optional] 
**chat_id** | **str** |  | [optional] 
**topic** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**state** | [**AgStatePropertiesState**](AgStatePropertiesState.md) |  | 

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


