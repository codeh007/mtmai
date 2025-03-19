# ComponentGet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**label** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.component_get import ComponentGet

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentGet from a JSON string
component_get_instance = ComponentGet.from_json(json)
# print the JSON string representation of the object
print(ComponentGet.to_json())

# convert the object into a dict
component_get_dict = component_get_instance.to_dict()
# create an instance of ComponentGet from a dict
component_get_from_dict = ComponentGet.from_dict(component_get_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


