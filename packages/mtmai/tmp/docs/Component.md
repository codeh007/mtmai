# Component


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**label** | **str** |  | 
**description** | **str** |  | 
**provider** | **str** |  | 
**component_type** | **str** |  | 
**version** | **int** |  | 
**component_version** | **int** |  | 
**config** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.component import Component

# TODO update the JSON string below
json = "{}"
# create an instance of Component from a JSON string
component_instance = Component.from_json(json)
# print the JSON string representation of the object
print(Component.to_json())

# convert the object into a dict
component_dict = component_instance.to_dict()
# create an instance of Component from a dict
component_from_dict = Component.from_dict(component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


