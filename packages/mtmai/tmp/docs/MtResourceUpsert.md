# MtResourceUpsert


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
from mtmai.clients.rest.models.mt_resource_upsert import MtResourceUpsert

# TODO update the JSON string below
json = "{}"
# create an instance of MtResourceUpsert from a JSON string
mt_resource_upsert_instance = MtResourceUpsert.from_json(json)
# print the JSON string representation of the object
print(MtResourceUpsert.to_json())

# convert the object into a dict
mt_resource_upsert_dict = mt_resource_upsert_instance.to_dict()
# create an instance of MtResourceUpsert from a dict
mt_resource_upsert_from_dict = MtResourceUpsert.from_dict(mt_resource_upsert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


