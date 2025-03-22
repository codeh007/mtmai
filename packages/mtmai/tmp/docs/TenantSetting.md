# TenantSetting


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the tenant setting | [optional] 

## Example

```python
from mtmai.clients.rest.models.tenant_setting import TenantSetting

# TODO update the JSON string below
json = "{}"
# create an instance of TenantSetting from a JSON string
tenant_setting_instance = TenantSetting.from_json(json)
# print the JSON string representation of the object
print(TenantSetting.to_json())

# convert the object into a dict
tenant_setting_dict = tenant_setting_instance.to_dict()
# create an instance of TenantSetting from a dict
tenant_setting_from_dict = TenantSetting.from_dict(tenant_setting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


