# AgStateList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[AgState]**](AgState.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.ag_state_list import AgStateList

# TODO update the JSON string below
json = "{}"
# create an instance of AgStateList from a JSON string
ag_state_list_instance = AgStateList.from_json(json)
# print the JSON string representation of the object
print(AgStateList.to_json())

# convert the object into a dict
ag_state_list_dict = ag_state_list_instance.to_dict()
# create an instance of AgStateList from a dict
ag_state_list_from_dict = AgStateList.from_dict(ag_state_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


