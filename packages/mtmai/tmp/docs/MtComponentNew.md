# MtComponentNew


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_component_new import MtComponentNew

# TODO update the JSON string below
json = "{}"
# create an instance of MtComponentNew from a JSON string
mt_component_new_instance = MtComponentNew.from_json(json)
# print the JSON string representation of the object
print(MtComponentNew.to_json())

# convert the object into a dict
mt_component_new_dict = mt_component_new_instance.to_dict()
# create an instance of MtComponentNew from a dict
mt_component_new_from_dict = MtComponentNew.from_dict(mt_component_new_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


