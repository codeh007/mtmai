# Worker


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | The name of the worker. | 
**type** | **str** |  | 
**last_heartbeat_at** | **datetime** | The time this worker last sent a heartbeat. | [optional] 
**last_listener_established** | **datetime** | The time this worker last sent a heartbeat. | [optional] 
**actions** | **List[str]** | The actions this worker can perform. | [optional] 
**slots** | [**List[SemaphoreSlots]**](SemaphoreSlots.md) | The semaphore slot state for the worker. | [optional] 
**recent_step_runs** | [**List[RecentStepRuns]**](RecentStepRuns.md) | The recent step runs for the worker. | [optional] 
**status** | **str** | The status of the worker. | [optional] 
**max_runs** | **int** | The maximum number of runs this worker can execute concurrently. | [optional] 
**available_runs** | **int** | The number of runs this worker can execute concurrently. | [optional] 
**dispatcher_id** | **str** | the id of the assigned dispatcher, in UUID format | [optional] 
**labels** | [**List[WorkerLabel]**](WorkerLabel.md) | The current label state of the worker. | [optional] 
**webhook_url** | **str** | The webhook URL for the worker. | [optional] 
**webhook_id** | **str** | The webhook ID for the worker. | [optional] 
**runtime_info** | [**WorkerRuntimeInfo**](WorkerRuntimeInfo.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.worker import Worker

# TODO update the JSON string below
json = "{}"
# create an instance of Worker from a JSON string
worker_instance = Worker.from_json(json)
# print the JSON string representation of the object
print(Worker.to_json())

# convert the object into a dict
worker_dict = worker_instance.to_dict()
# create an instance of Worker from a dict
worker_from_dict = Worker.from_dict(worker_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


