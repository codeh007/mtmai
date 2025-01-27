# TenantQueueMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | [**QueueMetrics**](QueueMetrics.md) | The total queue metrics. | [optional] 
**workflow** | [**Dict[str, QueueMetrics]**](QueueMetrics.md) |  | [optional] 
**queues** | **Dict[str, int]** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.tenant_queue_metrics import TenantQueueMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of TenantQueueMetrics from a JSON string
tenant_queue_metrics_instance = TenantQueueMetrics.from_json(json)
# print the JSON string representation of the object
print(TenantQueueMetrics.to_json())

# convert the object into a dict
tenant_queue_metrics_dict = tenant_queue_metrics_instance.to_dict()
# create an instance of TenantQueueMetrics from a dict
tenant_queue_metrics_from_dict = TenantQueueMetrics.from_dict(tenant_queue_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


