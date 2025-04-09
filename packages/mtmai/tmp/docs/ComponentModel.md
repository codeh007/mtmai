# ComponentModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** |  | [optional] 
**component_type** | **str** |  | [optional] 
**version** | **int** |  | [optional] 
**component_version** | **int** |  | [optional] 
**description** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**config** | **object** |  | [optional] 

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


