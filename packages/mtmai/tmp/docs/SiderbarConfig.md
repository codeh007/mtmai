# SiderbarConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**logo** | **str** | logo | [optional] 
**sideritems** | [**List[DashSidebarItem]**](DashSidebarItem.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.siderbar_config import SiderbarConfig

# TODO update the JSON string below
json = "{}"
# create an instance of SiderbarConfig from a JSON string
siderbar_config_instance = SiderbarConfig.from_json(json)
# print the JSON string representation of the object
print(SiderbarConfig.to_json())

# convert the object into a dict
siderbar_config_dict = siderbar_config_instance.to_dict()
# create an instance of SiderbarConfig from a dict
siderbar_config_from_dict = SiderbarConfig.from_dict(siderbar_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


