# TenantMemberList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[TenantMember]**](TenantMember.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.tenant_member_list import TenantMemberList

# TODO update the JSON string below
json = "{}"
# create an instance of TenantMemberList from a JSON string
tenant_member_list_instance = TenantMemberList.from_json(json)
# print the JSON string representation of the object
print(TenantMemberList.to_json())

# convert the object into a dict
tenant_member_list_dict = tenant_member_list_instance.to_dict()
# create an instance of TenantMemberList from a dict
tenant_member_list_from_dict = TenantMemberList.from_dict(tenant_member_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


