# UserTenantPublic


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email address of the user. | 
**name** | **str** | The display name of the user. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.user_tenant_public import UserTenantPublic

# TODO update the JSON string below
json = "{}"
# create an instance of UserTenantPublic from a JSON string
user_tenant_public_instance = UserTenantPublic.from_json(json)
# print the JSON string representation of the object
print(UserTenantPublic.to_json())

# convert the object into a dict
user_tenant_public_dict = user_tenant_public_instance.to_dict()
# create an instance of UserTenantPublic from a dict
user_tenant_public_from_dict = UserTenantPublic.from_dict(user_tenant_public_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


