# UserTenantMembershipsList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[TenantMember]**](TenantMember.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.user_tenant_memberships_list import UserTenantMembershipsList

# TODO update the JSON string below
json = "{}"
# create an instance of UserTenantMembershipsList from a JSON string
user_tenant_memberships_list_instance = UserTenantMembershipsList.from_json(json)
# print the JSON string representation of the object
print(UserTenantMembershipsList.to_json())

# convert the object into a dict
user_tenant_memberships_list_dict = user_tenant_memberships_list_instance.to_dict()
# create an instance of UserTenantMembershipsList from a dict
user_tenant_memberships_list_from_dict = UserTenantMembershipsList.from_dict(user_tenant_memberships_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


