# PlatformAccountUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | 
**email** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**token** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**platform** | **str** |  | 
**enabled** | **bool** |  | [optional] 
**comment** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**properties** | **object** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_account_update import PlatformAccountUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformAccountUpdate from a JSON string
platform_account_update_instance = PlatformAccountUpdate.from_json(json)
# print the JSON string representation of the object
print(PlatformAccountUpdate.to_json())

# convert the object into a dict
platform_account_update_dict = platform_account_update_instance.to_dict()
# create an instance of PlatformAccountUpdate from a dict
platform_account_update_from_dict = PlatformAccountUpdate.from_dict(platform_account_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


