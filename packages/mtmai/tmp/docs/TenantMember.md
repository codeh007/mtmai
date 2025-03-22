# TenantMember


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**user** | [**UserTenantPublic**](UserTenantPublic.md) | The user associated with this tenant member. | 
**role** | [**TenantMemberRole**](TenantMemberRole.md) | The role of the user in the tenant. | 
**tenant** | [**Tenant**](Tenant.md) | The tenant associated with this tenant member. | [optional] 

## Example

```python
from mtmai.clients.rest.models.tenant_member import TenantMember

# TODO update the JSON string below
json = "{}"
# create an instance of TenantMember from a JSON string
tenant_member_instance = TenantMember.from_json(json)
# print the JSON string representation of the object
print(TenantMember.to_json())

# convert the object into a dict
tenant_member_dict = tenant_member_instance.to_dict()
# create an instance of TenantMember from a dict
tenant_member_from_dict = TenantMember.from_dict(tenant_member_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


