# ComponentModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** | Describes how the component can be instantiated. | 
**component_type** | [**ComponentTypes**](ComponentTypes.md) | Logical type of the component. If missing, the component assumes the default type of the provider. | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | [optional] 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | [optional] 
**description** | **str** | Description of the component. | [optional] 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | [optional] 
**config** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.component_model import ComponentModel

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentModel from a JSON string
component_model_instance = ComponentModel.from_json(json)
# print the JSON string representation of the object
print(ComponentModel.to_json())

# convert the object into a dict
component_model_dict = component_model_instance.to_dict()
# create an instance of ComponentModel from a dict
component_model_from_dict = ComponentModel.from_dict(component_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


