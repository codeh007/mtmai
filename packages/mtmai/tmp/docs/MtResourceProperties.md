# MtResourceProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The resource title | 
**description** | **str** | The resource description | [optional] 
**version** | **str** | The resource version | [optional] 
**url** | **str** | The resource url | [optional] 
**type** | **str** | The resource type | 
**content** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_resource_properties import MtResourceProperties

# TODO update the JSON string below
json = "{}"
# create an instance of MtResourceProperties from a JSON string
mt_resource_properties_instance = MtResourceProperties.from_json(json)
# print the JSON string representation of the object
print(MtResourceProperties.to_json())

# convert the object into a dict
mt_resource_properties_dict = mt_resource_properties_instance.to_dict()
# create an instance of MtResourceProperties from a dict
mt_resource_properties_from_dict = MtResourceProperties.from_dict(mt_resource_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


