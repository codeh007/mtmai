# StepRunDiff


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | 
**original** | **str** |  | 
**modified** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.step_run_diff import StepRunDiff

# TODO update the JSON string below
json = "{}"
# create an instance of StepRunDiff from a JSON string
step_run_diff_instance = StepRunDiff.from_json(json)
# print the JSON string representation of the object
print(StepRunDiff.to_json())

# convert the object into a dict
step_run_diff_dict = step_run_diff_instance.to_dict()
# create an instance of StepRunDiff from a dict
step_run_diff_from_dict = StepRunDiff.from_dict(step_run_diff_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


