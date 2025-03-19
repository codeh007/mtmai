# ModelRunProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request** | **Dict[str, str]** |  | [optional] 
**response** | **Dict[str, str]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.model_run_properties import ModelRunProperties

# TODO update the JSON string below
json = "{}"
# create an instance of ModelRunProperties from a JSON string
model_run_properties_instance = ModelRunProperties.from_json(json)
# print the JSON string representation of the object
print(ModelRunProperties.to_json())

# convert the object into a dict
model_run_properties_dict = model_run_properties_instance.to_dict()
# create an instance of ModelRunProperties from a dict
model_run_properties_from_dict = ModelRunProperties.from_dict(model_run_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


