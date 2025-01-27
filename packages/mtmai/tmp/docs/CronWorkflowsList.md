# CronWorkflowsList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rows** | [**List[CronWorkflows]**](CronWorkflows.md) |  | [optional] 
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.cron_workflows_list import CronWorkflowsList

# TODO update the JSON string below
json = "{}"
# create an instance of CronWorkflowsList from a JSON string
cron_workflows_list_instance = CronWorkflowsList.from_json(json)
# print the JSON string representation of the object
print(CronWorkflowsList.to_json())

# convert the object into a dict
cron_workflows_list_dict = cron_workflows_list_instance.to_dict()
# create an instance of CronWorkflowsList from a dict
cron_workflows_list_from_dict = CronWorkflowsList.from_dict(cron_workflows_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


