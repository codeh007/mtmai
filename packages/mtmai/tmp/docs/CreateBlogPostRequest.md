# CreateBlogPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**blog_id** | **str** | The blog id. | 
**author_id** | **str** | The authord id. | [optional] 
**title** | **str** |  | 
**content** | **str** | The tenant associated with this tenant blog. | 

## Example

```python
from mtmaisdk.clients.rest.models.create_blog_post_request import CreateBlogPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBlogPostRequest from a JSON string
create_blog_post_request_instance = CreateBlogPostRequest.from_json(json)
# print the JSON string representation of the object
print(CreateBlogPostRequest.to_json())

# convert the object into a dict
create_blog_post_request_dict = create_blog_post_request_instance.to_dict()
# create an instance of CreateBlogPostRequest from a dict
create_blog_post_request_from_dict = CreateBlogPostRequest.from_dict(create_blog_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


