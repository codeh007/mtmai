# Step


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**readable_id** | **str** | The readable id of the step. | 
**tenant_id** | **str** |  | 
**job_id** | **str** |  | 
**action** | **str** |  | 
**timeout** | **str** | The timeout of the step. | [optional] 
**children** | **List[str]** |  | [optional] 
**parents** | **List[str]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.step import Step

# TODO update the JSON string below
json = "{}"
# create an instance of Step from a JSON string
step_instance = Step.from_json(json)
# print the JSON string representation of the object
print(Step.to_json())

# convert the object into a dict
step_dict = step_instance.to_dict()
# create an instance of Step from a dict
step_from_dict = Step.from_dict(step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


