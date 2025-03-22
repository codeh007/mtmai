# ImageContent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 
**alt** | **str** |  | [optional] 
**data** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.image_content import ImageContent

# TODO update the JSON string below
json = "{}"
# create an instance of ImageContent from a JSON string
image_content_instance = ImageContent.from_json(json)
# print the JSON string representation of the object
print(ImageContent.to_json())

# convert the object into a dict
image_content_dict = image_content_instance.to_dict()
# create an instance of ImageContent from a dict
image_content_from_dict = ImageContent.from_dict(image_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


