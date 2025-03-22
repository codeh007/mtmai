# MtResourceList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**rows** | [**List[MtResource]**](MtResource.md) |  | [optional] 
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_resource_list import MtResourceList

# TODO update the JSON string below
json = "{}"
# create an instance of MtResourceList from a JSON string
mt_resource_list_instance = MtResourceList.from_json(json)
# print the JSON string representation of the object
print(MtResourceList.to_json())

# convert the object into a dict
mt_resource_list_dict = mt_resource_list_instance.to_dict()
# create an instance of MtResourceList from a dict
mt_resource_list_from_dict = MtResourceList.from_dict(mt_resource_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


