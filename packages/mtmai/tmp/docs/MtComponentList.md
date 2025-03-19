# MtComponentList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[MtComponent]**](MtComponent.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_component_list import MtComponentList

# TODO update the JSON string below
json = "{}"
# create an instance of MtComponentList from a JSON string
mt_component_list_instance = MtComponentList.from_json(json)
# print the JSON string representation of the object
print(MtComponentList.to_json())

# convert the object into a dict
mt_component_list_dict = mt_component_list_instance.to_dict()
# create an instance of MtComponentList from a dict
mt_component_list_from_dict = MtComponentList.from_dict(mt_component_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


