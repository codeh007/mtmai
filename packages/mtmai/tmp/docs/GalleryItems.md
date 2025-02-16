# GalleryItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**teams** | [**List[ComponentModel]**](ComponentModel.md) |  | 
**components** | [**GalleryComponents**](GalleryComponents.md) |  | 

## Example

```python
from mtmai.clients.rest.models.gallery_items import GalleryItems

# TODO update the JSON string below
json = "{}"
# create an instance of GalleryItems from a JSON string
gallery_items_instance = GalleryItems.from_json(json)
# print the JSON string representation of the object
print(GalleryItems.to_json())

# convert the object into a dict
gallery_items_dict = gallery_items_instance.to_dict()
# create an instance of GalleryItems from a dict
gallery_items_from_dict = GalleryItems.from_dict(gallery_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


