# WorkerLabel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**key** | **str** | The key of the label. | 
**value** | **str** | The value of the label. | [optional] 

## Example

```python
from mtmai.clients.rest.models.worker_label import WorkerLabel

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerLabel from a JSON string
worker_label_instance = WorkerLabel.from_json(json)
# print the JSON string representation of the object
print(WorkerLabel.to_json())

# convert the object into a dict
worker_label_dict = worker_label_instance.to_dict()
# create an instance of WorkerLabel from a dict
worker_label_from_dict = WorkerLabel.from_dict(worker_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


