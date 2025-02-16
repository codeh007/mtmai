# CronWorkflows


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** |  | 
**workflow_version_id** | **str** |  | 
**workflow_id** | **str** |  | 
**workflow_name** | **str** |  | 
**cron** | **str** |  | 
**input** | **Dict[str, object]** |  | [optional] 
**additional_metadata** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.cron_workflows import CronWorkflows

# TODO update the JSON string below
json = "{}"
# create an instance of CronWorkflows from a JSON string
cron_workflows_instance = CronWorkflows.from_json(json)
# print the JSON string representation of the object
print(CronWorkflows.to_json())

# convert the object into a dict
cron_workflows_dict = cron_workflows_instance.to_dict()
# create an instance of CronWorkflows from a dict
cron_workflows_from_dict = CronWorkflows.from_dict(cron_workflows_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


