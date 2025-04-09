# GalleryMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author** | **str** |  | 
**created_at** | **str** |  | 
**updated_at** | **str** |  | 
**version** | **str** |  | 
**description** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**license** | **str** |  | [optional] 
**homepage** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**last_synced** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.gallery_metadata import GalleryMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of GalleryMetadata from a JSON string
gallery_metadata_instance = GalleryMetadata.from_json(json)
# print the JSON string representation of the object
print(GalleryMetadata.to_json())

# convert the object into a dict
gallery_metadata_dict = gallery_metadata_instance.to_dict()
# create an instance of GalleryMetadata from a dict
gallery_metadata_from_dict = GalleryMetadata.from_dict(gallery_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


