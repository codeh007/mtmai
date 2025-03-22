# CreatePullRequestFromStepRun


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**branch_name** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.create_pull_request_from_step_run import CreatePullRequestFromStepRun

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePullRequestFromStepRun from a JSON string
create_pull_request_from_step_run_instance = CreatePullRequestFromStepRun.from_json(json)
# print the JSON string representation of the object
print(CreatePullRequestFromStepRun.to_json())

# convert the object into a dict
create_pull_request_from_step_run_dict = create_pull_request_from_step_run_instance.to_dict()
# create an instance of CreatePullRequestFromStepRun from a dict
create_pull_request_from_step_run_from_dict = CreatePullRequestFromStepRun.from_dict(create_pull_request_from_step_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


