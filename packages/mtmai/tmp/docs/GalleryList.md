# GalleryList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Gallery]**](Gallery.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.gallery_list import GalleryList

# TODO update the JSON string below
json = "{}"
# create an instance of GalleryList from a JSON string
gallery_list_instance = GalleryList.from_json(json)
# print the JSON string representation of the object
print(GalleryList.to_json())

# convert the object into a dict
gallery_list_dict = gallery_list_instance.to_dict()
# create an instance of GalleryList from a dict
gallery_list_from_dict = GalleryList.from_dict(gallery_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


