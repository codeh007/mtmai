# CreateTenantAlertEmailGroupRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**emails** | **List[str]** | A list of emails for users | 

## Example

```python
from mtmaisdk.clients.rest.models.create_tenant_alert_email_group_request import CreateTenantAlertEmailGroupRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTenantAlertEmailGroupRequest from a JSON string
create_tenant_alert_email_group_request_instance = CreateTenantAlertEmailGroupRequest.from_json(json)
# print the JSON string representation of the object
print(CreateTenantAlertEmailGroupRequest.to_json())

# convert the object into a dict
create_tenant_alert_email_group_request_dict = create_tenant_alert_email_group_request_instance.to_dict()
# create an instance of CreateTenantAlertEmailGroupRequest from a dict
create_tenant_alert_email_group_request_from_dict = CreateTenantAlertEmailGroupRequest.from_dict(create_tenant_alert_email_group_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


