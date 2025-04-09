# APIResourceMetaProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 

## Example

```python
from mtmai.clients.rest.models.api_resource_meta_properties import APIResourceMetaProperties

# TODO update the JSON string below
json = "{}"
# create an instance of APIResourceMetaProperties from a JSON string
api_resource_meta_properties_instance = APIResourceMetaProperties.from_json(json)
# print the JSON string representation of the object
print(APIResourceMetaProperties.to_json())

# convert the object into a dict
api_resource_meta_properties_dict = api_resource_meta_properties_instance.to_dict()
# create an instance of APIResourceMetaProperties from a dict
api_resource_meta_properties_from_dict = APIResourceMetaProperties.from_dict(api_resource_meta_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


