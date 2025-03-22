# ModelRun


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**request** | **Dict[str, str]** |  | [optional] 
**response** | **Dict[str, str]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.model_run import ModelRun

# TODO update the JSON string below
json = "{}"
# create an instance of ModelRun from a JSON string
model_run_instance = ModelRun.from_json(json)
# print the JSON string representation of the object
print(ModelRun.to_json())

# convert the object into a dict
model_run_dict = model_run_instance.to_dict()
# create an instance of ModelRun from a dict
model_run_from_dict = ModelRun.from_dict(model_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


