# MtComponent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**id** | **str** | Unique identifier for the component. | [optional] 
**provider** | **str** |  | 
**component_type** | **str** |  | 
**version** | **int** |  | 
**component_version** | **int** |  | 
**description** | **str** |  | 
**label** | **str** |  | 
**config** | **Dict[str, object]** |  | 
**gallery_id** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.mt_component import MtComponent

# TODO update the JSON string below
json = "{}"
# create an instance of MtComponent from a JSON string
mt_component_instance = MtComponent.from_json(json)
# print the JSON string representation of the object
print(MtComponent.to_json())

# convert the object into a dict
mt_component_dict = mt_component_instance.to_dict()
# create an instance of MtComponent from a dict
mt_component_from_dict = MtComponent.from_dict(mt_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


