# TenantAlertingSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**alert_member_emails** | **bool** | Whether to alert tenant members. | [optional] 
**enable_workflow_run_failure_alerts** | **bool** | Whether to send alerts when workflow runs fail. | [optional] 
**enable_expiring_token_alerts** | **bool** | Whether to enable alerts when tokens are approaching expiration. | [optional] 
**enable_tenant_resource_limit_alerts** | **bool** | Whether to enable alerts when tenant resources are approaching limits. | [optional] 
**max_alerting_frequency** | **str** | The max frequency at which to alert. | 
**last_alerted_at** | **datetime** | The last time an alert was sent. | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.tenant_alerting_settings import TenantAlertingSettings

# TODO update the JSON string below
json = "{}"
# create an instance of TenantAlertingSettings from a JSON string
tenant_alerting_settings_instance = TenantAlertingSettings.from_json(json)
# print the JSON string representation of the object
print(TenantAlertingSettings.to_json())

# convert the object into a dict
tenant_alerting_settings_dict = tenant_alerting_settings_instance.to_dict()
# create an instance of TenantAlertingSettings from a dict
tenant_alerting_settings_from_dict = TenantAlertingSettings.from_dict(tenant_alerting_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


