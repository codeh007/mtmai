# EventKeyList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | **List[str]** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.event_key_list import EventKeyList

# TODO update the JSON string below
json = "{}"
# create an instance of EventKeyList from a JSON string
event_key_list_instance = EventKeyList.from_json(json)
# print the JSON string representation of the object
print(EventKeyList.to_json())

# convert the object into a dict
event_key_list_dict = event_key_list_instance.to_dict()
# create an instance of EventKeyList from a dict
event_key_list_from_dict = EventKeyList.from_dict(event_key_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


