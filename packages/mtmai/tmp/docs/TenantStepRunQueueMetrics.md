# TenantStepRunQueueMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queues** | **Dict[str, int]** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.tenant_step_run_queue_metrics import TenantStepRunQueueMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of TenantStepRunQueueMetrics from a JSON string
tenant_step_run_queue_metrics_instance = TenantStepRunQueueMetrics.from_json(json)
# print the JSON string representation of the object
print(TenantStepRunQueueMetrics.to_json())

# convert the object into a dict
tenant_step_run_queue_metrics_dict = tenant_step_run_queue_metrics_instance.to_dict()
# create an instance of TenantStepRunQueueMetrics from a dict
tenant_step_run_queue_metrics_from_dict = TenantStepRunQueueMetrics.from_dict(tenant_step_run_queue_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


