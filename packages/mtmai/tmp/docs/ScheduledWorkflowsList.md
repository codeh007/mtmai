# ScheduledWorkflowsList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rows** | [**List[ScheduledWorkflows]**](ScheduledWorkflows.md) |  | [optional] 
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.scheduled_workflows_list import ScheduledWorkflowsList

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduledWorkflowsList from a JSON string
scheduled_workflows_list_instance = ScheduledWorkflowsList.from_json(json)
# print the JSON string representation of the object
print(ScheduledWorkflowsList.to_json())

# convert the object into a dict
scheduled_workflows_list_dict = scheduled_workflows_list_instance.to_dict()
# create an instance of ScheduledWorkflowsList from a dict
scheduled_workflows_list_from_dict = ScheduledWorkflowsList.from_dict(scheduled_workflows_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


