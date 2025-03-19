# TenantInvite


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**email** | **str** | The email of the user to invite. | 
**role** | [**TenantMemberRole**](TenantMemberRole.md) | The role of the user in the tenant. | 
**tenant_id** | **str** | The tenant id associated with this tenant invite. | 
**tenant_name** | **str** | The tenant name for the tenant. | [optional] 
**expires** | **datetime** | The time that this invite expires. | 

## Example

```python
from mtmai.clients.rest.models.tenant_invite import TenantInvite

# TODO update the JSON string below
json = "{}"
# create an instance of TenantInvite from a JSON string
tenant_invite_instance = TenantInvite.from_json(json)
# print the JSON string representation of the object
print(TenantInvite.to_json())

# convert the object into a dict
tenant_invite_dict = tenant_invite_instance.to_dict()
# create an instance of TenantInvite from a dict
tenant_invite_from_dict = TenantInvite.from_dict(tenant_invite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


