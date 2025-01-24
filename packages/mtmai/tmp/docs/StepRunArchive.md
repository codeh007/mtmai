# StepRunArchive


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**step_run_id** | **str** |  | 
**order** | **int** |  | 
**input** | **str** |  | [optional] 
**output** | **str** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**error** | **str** |  | [optional] 
**retry_count** | **int** |  | 
**created_at** | **datetime** |  | 
**started_at_epoch** | **int** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**finished_at_epoch** | **int** |  | [optional] 
**timeout_at** | **datetime** |  | [optional] 
**timeout_at_epoch** | **int** |  | [optional] 
**cancelled_at** | **datetime** |  | [optional] 
**cancelled_at_epoch** | **int** |  | [optional] 
**cancelled_reason** | **str** |  | [optional] 
**cancelled_error** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.step_run_archive import StepRunArchive

# TODO update the JSON string below
json = "{}"
# create an instance of StepRunArchive from a JSON string
step_run_archive_instance = StepRunArchive.from_json(json)
# print the JSON string representation of the object
print(StepRunArchive.to_json())

# convert the object into a dict
step_run_archive_dict = step_run_archive_instance.to_dict()
# create an instance of StepRunArchive from a dict
step_run_archive_from_dict = StepRunArchive.from_dict(step_run_archive_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


