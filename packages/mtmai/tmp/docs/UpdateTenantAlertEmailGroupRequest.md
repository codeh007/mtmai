# UpdateTenantAlertEmailGroupRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**emails** | **List[str]** | A list of emails for users | 

## Example

```python
from mtmai.gomtmclients.rest.models.update_tenant_alert_email_group_request import UpdateTenantAlertEmailGroupRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTenantAlertEmailGroupRequest from a JSON string
update_tenant_alert_email_group_request_instance = UpdateTenantAlertEmailGroupRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateTenantAlertEmailGroupRequest.to_json())

# convert the object into a dict
update_tenant_alert_email_group_request_dict = update_tenant_alert_email_group_request_instance.to_dict()
# create an instance of UpdateTenantAlertEmailGroupRequest from a dict
update_tenant_alert_email_group_request_from_dict = UpdateTenantAlertEmailGroupRequest.from_dict(update_tenant_alert_email_group_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


