# AssisantList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Assisant]**](Assisant.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.assisant_list import AssisantList

# TODO update the JSON string below
json = "{}"
# create an instance of AssisantList from a JSON string
assisant_list_instance = AssisantList.from_json(json)
# print the JSON string representation of the object
print(AssisantList.to_json())

# convert the object into a dict
assisant_list_dict = assisant_list_instance.to_dict()
# create an instance of AssisantList from a dict
assisant_list_from_dict = AssisantList.from_dict(assisant_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


