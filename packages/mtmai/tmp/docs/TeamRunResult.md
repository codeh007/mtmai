# TeamRunResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_run** | [**WorkflowRun**](WorkflowRun.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.team_run_result import TeamRunResult

# TODO update the JSON string below
json = "{}"
# create an instance of TeamRunResult from a JSON string
team_run_result_instance = TeamRunResult.from_json(json)
# print the JSON string representation of the object
print(TeamRunResult.to_json())

# convert the object into a dict
team_run_result_dict = team_run_result_instance.to_dict()
# create an instance of TeamRunResult from a dict
team_run_result_from_dict = TeamRunResult.from_dict(team_run_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


