# ModelContext


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**some** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.model_context import ModelContext

# TODO update the JSON string below
json = "{}"
# create an instance of ModelContext from a JSON string
model_context_instance = ModelContext.from_json(json)
# print the JSON string representation of the object
print(ModelContext.to_json())

# convert the object into a dict
model_context_dict = model_context_instance.to_dict()
# create an instance of ModelContext from a dict
model_context_from_dict = ModelContext.from_dict(model_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


