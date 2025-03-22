# PlatformUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**url** | **str** |  | 
**login_url** | **str** |  | [optional] 
**properties** | **object** |  | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_update import PlatformUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformUpdate from a JSON string
platform_update_instance = PlatformUpdate.from_json(json)
# print the JSON string representation of the object
print(PlatformUpdate.to_json())

# convert the object into a dict
platform_update_dict = platform_update_instance.to_dict()
# create an instance of PlatformUpdate from a dict
platform_update_from_dict = PlatformUpdate.from_dict(platform_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


