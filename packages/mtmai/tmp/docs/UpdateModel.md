# UpdateModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.update_model import UpdateModel

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateModel from a JSON string
update_model_instance = UpdateModel.from_json(json)
# print the JSON string representation of the object
print(UpdateModel.to_json())

# convert the object into a dict
update_model_dict = update_model_instance.to_dict()
# create an instance of UpdateModel from a dict
update_model_from_dict = UpdateModel.from_dict(update_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


