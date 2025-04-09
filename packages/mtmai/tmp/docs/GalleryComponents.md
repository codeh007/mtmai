# GalleryComponents


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agents** | **List[Dict[str, object]]** |  | 
**models** | **List[Dict[str, object]]** |  | 
**tools** | **List[Dict[str, object]]** |  | 
**terminations** | **List[Dict[str, object]]** |  | 

## Example

```python
from mtmai.clients.rest.models.gallery_components import GalleryComponents

# TODO update the JSON string below
json = "{}"
# create an instance of GalleryComponents from a JSON string
gallery_components_instance = GalleryComponents.from_json(json)
# print the JSON string representation of the object
print(GalleryComponents.to_json())

# convert the object into a dict
gallery_components_dict = gallery_components_instance.to_dict()
# create an instance of GalleryComponents from a dict
gallery_components_from_dict = GalleryComponents.from_dict(gallery_components_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


