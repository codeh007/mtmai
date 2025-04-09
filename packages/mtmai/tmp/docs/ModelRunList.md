# ModelRunList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[ModelRun]**](ModelRun.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.model_run_list import ModelRunList

# TODO update the JSON string below
json = "{}"
# create an instance of ModelRunList from a JSON string
model_run_list_instance = ModelRunList.from_json(json)
# print the JSON string representation of the object
print(ModelRunList.to_json())

# convert the object into a dict
model_run_list_dict = model_run_list_instance.to_dict()
# create an instance of ModelRunList from a dict
model_run_list_from_dict = ModelRunList.from_dict(model_run_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


