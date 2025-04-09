# ComponentList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Component]**](Component.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.component_list import ComponentList

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentList from a JSON string
component_list_instance = ComponentList.from_json(json)
# print the JSON string representation of the object
print(ComponentList.to_json())

# convert the object into a dict
component_list_dict = component_list_instance.to_dict()
# create an instance of ComponentList from a dict
component_list_from_dict = ComponentList.from_dict(component_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


