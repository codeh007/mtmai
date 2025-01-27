# TenantAlertEmailGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**emails** | **List[str]** | A list of emails for users | 

## Example

```python
from mtmaisdk.clients.rest.models.tenant_alert_email_group import TenantAlertEmailGroup

# TODO update the JSON string below
json = "{}"
# create an instance of TenantAlertEmailGroup from a JSON string
tenant_alert_email_group_instance = TenantAlertEmailGroup.from_json(json)
# print the JSON string representation of the object
print(TenantAlertEmailGroup.to_json())

# convert the object into a dict
tenant_alert_email_group_dict = tenant_alert_email_group_instance.to_dict()
# create an instance of TenantAlertEmailGroup from a dict
tenant_alert_email_group_from_dict = TenantAlertEmailGroup.from_dict(tenant_alert_email_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


