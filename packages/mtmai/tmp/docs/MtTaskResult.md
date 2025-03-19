# MtTaskResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | **List[Dict[str, object]]** |  | 
**stop_reason** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.mt_task_result import MtTaskResult

# TODO update the JSON string below
json = "{}"
# create an instance of MtTaskResult from a JSON string
mt_task_result_instance = MtTaskResult.from_json(json)
# print the JSON string representation of the object
print(MtTaskResult.to_json())

# convert the object into a dict
mt_task_result_dict = mt_task_result_instance.to_dict()
# create an instance of MtTaskResult from a dict
mt_task_result_from_dict = MtTaskResult.from_dict(mt_task_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


