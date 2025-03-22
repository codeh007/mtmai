# Gallery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** |  | 
**url** | **str** |  | 
**author** | **str** |  | 
**homepage** | **str** |  | 
**description** | **str** |  | 
**tags** | **List[str]** |  | 
**license** | **str** |  | 
**last_synced** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.gallery import Gallery

# TODO update the JSON string below
json = "{}"
# create an instance of Gallery from a JSON string
gallery_instance = Gallery.from_json(json)
# print the JSON string representation of the object
print(Gallery.to_json())

# convert the object into a dict
gallery_dict = gallery_instance.to_dict()
# create an instance of Gallery from a dict
gallery_from_dict = Gallery.from_dict(gallery_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


