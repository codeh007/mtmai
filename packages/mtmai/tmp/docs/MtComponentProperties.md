# MtComponentProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**component_type** | [**ComponentTypes**](ComponentTypes.md) |  | 
**provider** | **str** |  | 
**label** | **str** |  | 
**description** | **str** |  | 
**version** | **int** |  | [default to 1]
**component_version** | **int** |  | [default to 1]
**gallery_id** | **str** |  | [optional] 
**config** | **Dict[str, object]** |  | 
**component** | [**MtComponentPropertiesComponent**](MtComponentPropertiesComponent.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_component_properties import MtComponentProperties

# TODO update the JSON string below
json = "{}"
# create an instance of MtComponentProperties from a JSON string
mt_component_properties_instance = MtComponentProperties.from_json(json)
# print the JSON string representation of the object
print(MtComponentProperties.to_json())

# convert the object into a dict
mt_component_properties_dict = mt_component_properties_instance.to_dict()
# create an instance of MtComponentProperties from a dict
mt_component_properties_from_dict = MtComponentProperties.from_dict(mt_component_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


