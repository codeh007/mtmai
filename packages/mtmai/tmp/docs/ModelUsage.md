# ModelUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** |  | [optional] 
**prompt_tokens** | **int** |  | [optional] 
**completion_tokens** | **int** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.model_usage import ModelUsage

# TODO update the JSON string below
json = "{}"
# create an instance of ModelUsage from a JSON string
model_usage_instance = ModelUsage.from_json(json)
# print the JSON string representation of the object
print(ModelUsage.to_json())

# convert the object into a dict
model_usage_dict = model_usage_instance.to_dict()
# create an instance of ModelUsage from a dict
model_usage_from_dict = ModelUsage.from_dict(model_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


