# PlatformAccountData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**username** | **str** |  | [optional] 
**api_token** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_account_data import PlatformAccountData

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformAccountData from a JSON string
platform_account_data_instance = PlatformAccountData.from_json(json)
# print the JSON string representation of the object
print(PlatformAccountData.to_json())

# convert the object into a dict
platform_account_data_dict = platform_account_data_instance.to_dict()
# create an instance of PlatformAccountData from a dict
platform_account_data_from_dict = PlatformAccountData.from_dict(platform_account_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


