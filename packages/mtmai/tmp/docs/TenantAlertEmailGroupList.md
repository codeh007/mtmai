# TenantAlertEmailGroupList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[TenantAlertEmailGroup]**](TenantAlertEmailGroup.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.tenant_alert_email_group_list import TenantAlertEmailGroupList

# TODO update the JSON string below
json = "{}"
# create an instance of TenantAlertEmailGroupList from a JSON string
tenant_alert_email_group_list_instance = TenantAlertEmailGroupList.from_json(json)
# print the JSON string representation of the object
print(TenantAlertEmailGroupList.to_json())

# convert the object into a dict
tenant_alert_email_group_list_dict = tenant_alert_email_group_list_instance.to_dict()
# create an instance of TenantAlertEmailGroupList from a dict
tenant_alert_email_group_list_from_dict = TenantAlertEmailGroupList.from_dict(tenant_alert_email_group_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


