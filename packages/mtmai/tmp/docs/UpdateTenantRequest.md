# UpdateTenantRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the tenant. | [optional] 
**analytics_opt_out** | **bool** | Whether the tenant has opted out of analytics. | [optional] 
**alert_member_emails** | **bool** | Whether to alert tenant members. | [optional] 
**enable_workflow_run_failure_alerts** | **bool** | Whether to send alerts when workflow runs fail. | [optional] 
**enable_expiring_token_alerts** | **bool** | Whether to enable alerts when tokens are approaching expiration. | [optional] 
**enable_tenant_resource_limit_alerts** | **bool** | Whether to enable alerts when tenant resources are approaching limits. | [optional] 
**max_alerting_frequency** | **str** | The max frequency at which to alert. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.update_tenant_request import UpdateTenantRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTenantRequest from a JSON string
update_tenant_request_instance = UpdateTenantRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateTenantRequest.to_json())

# convert the object into a dict
update_tenant_request_dict = update_tenant_request_instance.to_dict()
# create an instance of UpdateTenantRequest from a dict
update_tenant_request_from_dict = UpdateTenantRequest.from_dict(update_tenant_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


