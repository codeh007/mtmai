# PlatformList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Platform]**](Platform.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_list import PlatformList

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformList from a JSON string
platform_list_instance = PlatformList.from_json(json)
# print the JSON string representation of the object
print(PlatformList.to_json())

# convert the object into a dict
platform_list_dict = platform_list_instance.to_dict()
# create an instance of PlatformList from a dict
platform_list_from_dict = PlatformList.from_dict(platform_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


