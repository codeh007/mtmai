# ComponentUpsert


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | 
**description** | **str** |  | 
**provider** | **str** |  | 
**component_type** | **str** |  | 
**version** | **int** |  | 
**component_version** | **int** |  | 
**config** | **object** |  | 

## Example

```python
from mtmai.clients.rest.models.component_upsert import ComponentUpsert

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentUpsert from a JSON string
component_upsert_instance = ComponentUpsert.from_json(json)
# print the JSON string representation of the object
print(ComponentUpsert.to_json())

# convert the object into a dict
component_upsert_dict = component_upsert_instance.to_dict()
# create an instance of ComponentUpsert from a dict
component_upsert_from_dict = ComponentUpsert.from_dict(component_upsert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


