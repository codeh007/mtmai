# Workflow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | The name of the workflow. | 
**description** | **str** | The description of the workflow. | [optional] 
**is_paused** | **bool** | Whether the workflow is paused. | [optional] 
**versions** | [**List[WorkflowVersionMeta]**](WorkflowVersionMeta.md) |  | [optional] 
**tags** | [**List[WorkflowTag]**](WorkflowTag.md) | The tags of the workflow. | [optional] 
**jobs** | [**List[Job]**](Job.md) | The jobs of the workflow. | [optional] 

## Example

```python
from mtmai.clients.rest.models.workflow import Workflow

# TODO update the JSON string below
json = "{}"
# create an instance of Workflow from a JSON string
workflow_instance = Workflow.from_json(json)
# print the JSON string representation of the object
print(Workflow.to_json())

# convert the object into a dict
workflow_dict = workflow_instance.to_dict()
# create an instance of Workflow from a dict
workflow_from_dict = Workflow.from_dict(workflow_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


