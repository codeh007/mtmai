# PlatformAccountCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**username** | **str** |  | 
**email** | **str** |  | [optional] 
**password** | **str** |  | 
**token** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**platform** | **str** |  | 
**enabled** | **bool** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**state** | **Dict[str, object]** |  | [optional] 
**error** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_account_create import PlatformAccountCreate

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformAccountCreate from a JSON string
platform_account_create_instance = PlatformAccountCreate.from_json(json)
# print the JSON string representation of the object
print(PlatformAccountCreate.to_json())

# convert the object into a dict
platform_account_create_dict = platform_account_create_instance.to_dict()
# create an instance of PlatformAccountCreate from a dict
platform_account_create_from_dict = PlatformAccountCreate.from_dict(platform_account_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


