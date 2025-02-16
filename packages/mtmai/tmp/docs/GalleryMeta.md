# GalleryMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author** | **str** |  | 
**created_at** | **str** |  | 
**updated_at** | **str** |  | 
**version** | **str** |  | 
**description** | **str** |  | [optional] 
**tags** | **List[object]** |  | [optional] 
**license** | **str** |  | [optional] 
**homepage** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**last_synced** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.gallery_meta import GalleryMeta

# TODO update the JSON string below
json = "{}"
# create an instance of GalleryMeta from a JSON string
gallery_meta_instance = GalleryMeta.from_json(json)
# print the JSON string representation of the object
print(GalleryMeta.to_json())

# convert the object into a dict
gallery_meta_dict = gallery_meta_instance.to_dict()
# create an instance of GalleryMeta from a dict
gallery_meta_from_dict = GalleryMeta.from_dict(gallery_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


