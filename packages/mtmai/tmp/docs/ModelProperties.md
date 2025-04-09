# ModelProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**model** | **str** |  | 
**provider** | **str** |  | 
**api_key** | **str** |  | 
**api_base** | **str** |  | 
**vendor** | **str** |  | 
**description** | **str** |  | [optional] 
**family** | **str** |  | 
**vision** | **bool** |  | 
**function_calling** | **bool** |  | 
**json_output** | **bool** |  | 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.model_properties import ModelProperties

# TODO update the JSON string below
json = "{}"
# create an instance of ModelProperties from a JSON string
model_properties_instance = ModelProperties.from_json(json)
# print the JSON string representation of the object
print(ModelProperties.to_json())

# convert the object into a dict
model_properties_dict = model_properties_instance.to_dict()
# create an instance of ModelProperties from a dict
model_properties_from_dict = ModelProperties.from_dict(model_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


