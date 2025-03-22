# UpsertModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**provider** | **str** |  | 
**api_key** | **str** |  | 
**api_base** | **str** |  | 
**vendor** | **str** |  | 
**description** | **str** |  | [optional] 
**family** | **str** |  | 
**vision** | **bool** |  | 
**function_calling** | **bool** |  | 
**json_output** | **bool** |  | 

## Example

```python
from mtmai.clients.rest.models.upsert_model import UpsertModel

# TODO update the JSON string below
json = "{}"
# create an instance of UpsertModel from a JSON string
upsert_model_instance = UpsertModel.from_json(json)
# print the JSON string representation of the object
print(UpsertModel.to_json())

# convert the object into a dict
upsert_model_dict = upsert_model_instance.to_dict()
# create an instance of UpsertModel from a dict
upsert_model_from_dict = UpsertModel.from_dict(upsert_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


