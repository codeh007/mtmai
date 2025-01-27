# StepRunArchiveList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[StepRunArchive]**](StepRunArchive.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.step_run_archive_list import StepRunArchiveList

# TODO update the JSON string below
json = "{}"
# create an instance of StepRunArchiveList from a JSON string
step_run_archive_list_instance = StepRunArchiveList.from_json(json)
# print the JSON string representation of the object
print(StepRunArchiveList.to_json())

# convert the object into a dict
step_run_archive_list_dict = step_run_archive_list_instance.to_dict()
# create an instance of StepRunArchiveList from a dict
step_run_archive_list_from_dict = StepRunArchiveList.from_dict(step_run_archive_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


