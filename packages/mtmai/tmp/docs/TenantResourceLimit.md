# TenantResourceLimit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**resource** | [**TenantResource**](TenantResource.md) | The resource associated with this limit. | 
**limit_value** | **int** | The limit associated with this limit. | 
**alarm_value** | **int** | The alarm value associated with this limit to warn of approaching limit value. | [optional] 
**value** | **int** | The current value associated with this limit. | 
**window** | **str** | The meter window for the limit. (i.e. 1 day, 1 week, 1 month) | [optional] 
**last_refill** | **datetime** | The last time the limit was refilled. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.tenant_resource_limit import TenantResourceLimit

# TODO update the JSON string below
json = "{}"
# create an instance of TenantResourceLimit from a JSON string
tenant_resource_limit_instance = TenantResourceLimit.from_json(json)
# print the JSON string representation of the object
print(TenantResourceLimit.to_json())

# convert the object into a dict
tenant_resource_limit_dict = tenant_resource_limit_instance.to_dict()
# create an instance of TenantResourceLimit from a dict
tenant_resource_limit_from_dict = TenantResourceLimit.from_dict(tenant_resource_limit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


