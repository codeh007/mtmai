# LogLineList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[LogLine]**](LogLine.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.log_line_list import LogLineList

# TODO update the JSON string below
json = "{}"
# create an instance of LogLineList from a JSON string
log_line_list_instance = LogLineList.from_json(json)
# print the JSON string representation of the object
print(LogLineList.to_json())

# convert the object into a dict
log_line_list_dict = log_line_list_instance.to_dict()
# create an instance of LogLineList from a dict
log_line_list_from_dict = LogLineList.from_dict(log_line_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


