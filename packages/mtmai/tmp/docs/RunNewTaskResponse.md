# RunNewTaskResponse

运行新任务的结果

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.run_new_task_response import RunNewTaskResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RunNewTaskResponse from a JSON string
run_new_task_response_instance = RunNewTaskResponse.from_json(json)
# print the JSON string representation of the object
print(RunNewTaskResponse.to_json())

# convert the object into a dict
run_new_task_response_dict = run_new_task_response_instance.to_dict()
# create an instance of RunNewTaskResponse from a dict
run_new_task_response_from_dict = RunNewTaskResponse.from_dict(run_new_task_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


