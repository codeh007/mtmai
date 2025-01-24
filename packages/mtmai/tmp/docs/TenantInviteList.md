# TenantInviteList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[TenantInvite]**](TenantInvite.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.tenant_invite_list import TenantInviteList

# TODO update the JSON string below
json = "{}"
# create an instance of TenantInviteList from a JSON string
tenant_invite_list_instance = TenantInviteList.from_json(json)
# print the JSON string representation of the object
print(TenantInviteList.to_json())

# convert the object into a dict
tenant_invite_list_dict = tenant_invite_list_instance.to_dict()
# create an instance of TenantInviteList from a dict
tenant_invite_list_from_dict = TenantInviteList.from_dict(tenant_invite_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


