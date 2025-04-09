# ComponentProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | 
**description** | **str** |  | 
**provider** | **str** |  | 
**component_type** | **str** |  | 
**version** | **int** |  | 
**component_version** | **int** |  | 
**config** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.component_properties import ComponentProperties

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentProperties from a JSON string
component_properties_instance = ComponentProperties.from_json(json)
# print the JSON string representation of the object
print(ComponentProperties.to_json())

# convert the object into a dict
component_properties_dict = component_properties_instance.to_dict()
# create an instance of ComponentProperties from a dict
component_properties_from_dict = ComponentProperties.from_dict(component_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


