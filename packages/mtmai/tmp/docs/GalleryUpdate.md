# GalleryUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** |  | 
**user_id** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.gallery_update import GalleryUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of GalleryUpdate from a JSON string
gallery_update_instance = GalleryUpdate.from_json(json)
# print the JSON string representation of the object
print(GalleryUpdate.to_json())

# convert the object into a dict
gallery_update_dict = gallery_update_instance.to_dict()
# create an instance of GalleryUpdate from a dict
gallery_update_from_dict = GalleryUpdate.from_dict(gallery_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


