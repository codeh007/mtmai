# GetStepRunDiffResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**diffs** | [**List[StepRunDiff]**](StepRunDiff.md) |  | 

## Example

```python
from mtmai.clients.rest.models.get_step_run_diff_response import GetStepRunDiffResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetStepRunDiffResponse from a JSON string
get_step_run_diff_response_instance = GetStepRunDiffResponse.from_json(json)
# print the JSON string representation of the object
print(GetStepRunDiffResponse.to_json())

# convert the object into a dict
get_step_run_diff_response_dict = get_step_run_diff_response_instance.to_dict()
# create an instance of GetStepRunDiffResponse from a dict
get_step_run_diff_response_from_dict = GetStepRunDiffResponse.from_dict(get_step_run_diff_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


