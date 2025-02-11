# QueueMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**num_queued** | **int** | The number of items in the queue. | 
**num_running** | **int** | The number of items running. | 
**num_pending** | **int** | The number of items pending. | 

## Example

```python
from mtmaisdk.clients.rest.models.queue_metrics import QueueMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of QueueMetrics from a JSON string
queue_metrics_instance = QueueMetrics.from_json(json)
# print the JSON string representation of the object
print(QueueMetrics.to_json())

# convert the object into a dict
queue_metrics_dict = queue_metrics_instance.to_dict()
# create an instance of QueueMetrics from a dict
queue_metrics_from_dict = QueueMetrics.from_dict(queue_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


