# WorkerRuntimeInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sdk_version** | **str** |  | [optional] 
**language** | [**WorkerRuntimeSDKs**](WorkerRuntimeSDKs.md) |  | [optional] 
**language_version** | **str** |  | [optional] 
**os** | **str** |  | [optional] 
**runtime_extra** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.worker_runtime_info import WorkerRuntimeInfo

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerRuntimeInfo from a JSON string
worker_runtime_info_instance = WorkerRuntimeInfo.from_json(json)
# print the JSON string representation of the object
print(WorkerRuntimeInfo.to_json())

# convert the object into a dict
worker_runtime_info_dict = worker_runtime_info_instance.to_dict()
# create an instance of WorkerRuntimeInfo from a dict
worker_runtime_info_from_dict = WorkerRuntimeInfo.from_dict(worker_runtime_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


