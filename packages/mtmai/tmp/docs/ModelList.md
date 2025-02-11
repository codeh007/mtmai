# ModelList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Model]**](Model.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.model_list import ModelList

# TODO update the JSON string below
json = "{}"
# create an instance of ModelList from a JSON string
model_list_instance = ModelList.from_json(json)
# print the JSON string representation of the object
print(ModelList.to_json())

# convert the object into a dict
model_list_dict = model_list_instance.to_dict()
# create an instance of ModelList from a dict
model_list_from_dict = ModelList.from_dict(model_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


