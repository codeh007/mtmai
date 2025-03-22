# MtComponentProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the component. | [optional] 
**provider** | **str** | Describes how the component can be instantiated. | 
**component_type** | **str** |  | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | 
**description** | **str** | Description of the component. | 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | 
**config** | [**ModelConfig**](ModelConfig.md) |  | 

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


