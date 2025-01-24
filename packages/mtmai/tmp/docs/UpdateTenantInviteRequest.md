# UpdateTenantInviteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role** | [**TenantMemberRole**](TenantMemberRole.md) | The role of the user in the tenant. | 

## Example

```python
from mtmai.gomtmclients.rest.models.update_tenant_invite_request import UpdateTenantInviteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTenantInviteRequest from a JSON string
update_tenant_invite_request_instance = UpdateTenantInviteRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateTenantInviteRequest.to_json())

# convert the object into a dict
update_tenant_invite_request_dict = update_tenant_invite_request_instance.to_dict()
# create an instance of UpdateTenantInviteRequest from a dict
update_tenant_invite_request_from_dict = UpdateTenantInviteRequest.from_dict(update_tenant_invite_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


