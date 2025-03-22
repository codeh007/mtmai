# AgEventList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[AgEvent]**](AgEvent.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.ag_event_list import AgEventList

# TODO update the JSON string below
json = "{}"
# create an instance of AgEventList from a JSON string
ag_event_list_instance = AgEventList.from_json(json)
# print the JSON string representation of the object
print(AgEventList.to_json())

# convert the object into a dict
ag_event_list_dict = ag_event_list_instance.to_dict()
# create an instance of AgEventList from a dict
ag_event_list_from_dict = AgEventList.from_dict(ag_event_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


