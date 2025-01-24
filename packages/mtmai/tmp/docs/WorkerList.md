# WorkerList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Worker]**](Worker.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.worker_list import WorkerList

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerList from a JSON string
worker_list_instance = WorkerList.from_json(json)
# print the JSON string representation of the object
print(WorkerList.to_json())

# convert the object into a dict
worker_list_dict = worker_list_instance.to_dict()
# create an instance of WorkerList from a dict
worker_list_from_dict = WorkerList.from_dict(worker_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


