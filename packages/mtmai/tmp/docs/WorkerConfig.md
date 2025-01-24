# WorkerConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**worker_token** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.worker_config import WorkerConfig

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerConfig from a JSON string
worker_config_instance = WorkerConfig.from_json(json)
# print the JSON string representation of the object
print(WorkerConfig.to_json())

# convert the object into a dict
worker_config_dict = worker_config_instance.to_dict()
# create an instance of WorkerConfig from a dict
worker_config_from_dict = WorkerConfig.from_dict(worker_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


