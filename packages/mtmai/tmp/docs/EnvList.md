# EnvList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Env]**](Env.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.env_list import EnvList

# TODO update the JSON string below
json = "{}"
# create an instance of EnvList from a JSON string
env_list_instance = EnvList.from_json(json)
# print the JSON string representation of the object
print(EnvList.to_json())

# convert the object into a dict
env_list_dict = env_list_instance.to_dict()
# create an instance of EnvList from a dict
env_list_from_dict = EnvList.from_dict(env_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


