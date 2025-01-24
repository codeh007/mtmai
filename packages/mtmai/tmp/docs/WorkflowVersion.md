# WorkflowVersion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**version** | **str** | The version of the workflow. | 
**order** | **int** |  | 
**workflow_id** | **str** |  | 
**sticky** | **str** | The sticky strategy of the workflow. | [optional] 
**default_priority** | **int** | The default priority of the workflow. | [optional] 
**workflow** | [**Workflow**](Workflow.md) |  | [optional] 
**concurrency** | [**WorkflowConcurrency**](WorkflowConcurrency.md) |  | [optional] 
**triggers** | [**WorkflowTriggers**](WorkflowTriggers.md) |  | [optional] 
**schedule_timeout** | **str** |  | [optional] 
**jobs** | [**List[Job]**](Job.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.workflow_version import WorkflowVersion

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowVersion from a JSON string
workflow_version_instance = WorkflowVersion.from_json(json)
# print the JSON string representation of the object
print(WorkflowVersion.to_json())

# convert the object into a dict
workflow_version_dict = workflow_version_instance.to_dict()
# create an instance of WorkflowVersion from a dict
workflow_version_from_dict = WorkflowVersion.from_dict(workflow_version_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


