# MtResource


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | [optional] 
**title** | **str** | The resource title | 
**description** | **str** | The resource description | [optional] 
**version** | **str** | The resource version | [optional] 
**url** | **str** | The resource url | [optional] 
**type** | **str** | The resource type | 
**content** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_resource import MtResource

# TODO update the JSON string below
json = "{}"
# create an instance of MtResource from a JSON string
mt_resource_instance = MtResource.from_json(json)
# print the JSON string representation of the object
print(MtResource.to_json())

# convert the object into a dict
mt_resource_dict = mt_resource_instance.to_dict()
# create an instance of MtResource from a dict
mt_resource_from_dict = MtResource.from_dict(mt_resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


