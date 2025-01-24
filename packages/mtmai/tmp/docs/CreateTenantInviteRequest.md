# CreateTenantInviteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email of the user to invite. | 
**role** | [**TenantMemberRole**](TenantMemberRole.md) | The role of the user in the tenant. | 

## Example

```python
from mtmai.gomtmclients.rest.models.create_tenant_invite_request import CreateTenantInviteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTenantInviteRequest from a JSON string
create_tenant_invite_request_instance = CreateTenantInviteRequest.from_json(json)
# print the JSON string representation of the object
print(CreateTenantInviteRequest.to_json())

# convert the object into a dict
create_tenant_invite_request_dict = create_tenant_invite_request_instance.to_dict()
# create an instance of CreateTenantInviteRequest from a dict
create_tenant_invite_request_from_dict = CreateTenantInviteRequest.from_dict(create_tenant_invite_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


