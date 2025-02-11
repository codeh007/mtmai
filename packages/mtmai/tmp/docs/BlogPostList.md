# BlogPostList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[BlogPost]**](BlogPost.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.blog_post_list import BlogPostList

# TODO update the JSON string below
json = "{}"
# create an instance of BlogPostList from a JSON string
blog_post_list_instance = BlogPostList.from_json(json)
# print the JSON string representation of the object
print(BlogPostList.to_json())

# convert the object into a dict
blog_post_list_dict = blog_post_list_instance.to_dict()
# create an instance of BlogPostList from a dict
blog_post_list_from_dict = BlogPostList.from_dict(blog_post_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


