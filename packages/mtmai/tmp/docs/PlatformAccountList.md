# PlatformAccountList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[PlatformAccount]**](PlatformAccount.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_account_list import PlatformAccountList

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformAccountList from a JSON string
platform_account_list_instance = PlatformAccountList.from_json(json)
# print the JSON string representation of the object
print(PlatformAccountList.to_json())

# convert the object into a dict
platform_account_list_dict = platform_account_list_instance.to_dict()
# create an instance of PlatformAccountList from a dict
platform_account_list_from_dict = PlatformAccountList.from_dict(platform_account_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


