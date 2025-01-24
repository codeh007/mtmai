# TenantList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Tenant]**](Tenant.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.tenant_list import TenantList

# TODO update the JSON string below
json = "{}"
# create an instance of TenantList from a JSON string
tenant_list_instance = TenantList.from_json(json)
# print the JSON string representation of the object
print(TenantList.to_json())

# convert the object into a dict
tenant_list_dict = tenant_list_instance.to_dict()
# create an instance of TenantList from a dict
tenant_list_from_dict = TenantList.from_dict(tenant_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


