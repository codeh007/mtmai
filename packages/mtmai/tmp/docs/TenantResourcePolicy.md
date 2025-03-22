# TenantResourcePolicy


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limits** | [**List[TenantResourceLimit]**](TenantResourceLimit.md) | A list of resource limits for the tenant. | 

## Example

```python
from mtmai.clients.rest.models.tenant_resource_policy import TenantResourcePolicy

# TODO update the JSON string below
json = "{}"
# create an instance of TenantResourcePolicy from a JSON string
tenant_resource_policy_instance = TenantResourcePolicy.from_json(json)
# print the JSON string representation of the object
print(TenantResourcePolicy.to_json())

# convert the object into a dict
tenant_resource_policy_dict = tenant_resource_policy_instance.to_dict()
# create an instance of TenantResourcePolicy from a dict
tenant_resource_policy_from_dict = TenantResourcePolicy.from_dict(tenant_resource_policy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


