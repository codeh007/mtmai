# PlatformAccountProperties


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
from mtmai.clients.rest.models.platform_account_properties import PlatformAccountProperties

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformAccountProperties from a JSON string
platform_account_properties_instance = PlatformAccountProperties.from_json(json)
# print the JSON string representation of the object
print(PlatformAccountProperties.to_json())

# convert the object into a dict
platform_account_properties_dict = platform_account_properties_instance.to_dict()
# create an instance of PlatformAccountProperties from a dict
platform_account_properties_from_dict = PlatformAccountProperties.from_dict(platform_account_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


