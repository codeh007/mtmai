# BlogPost


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**title** | **str** |  | 
**content** | **str** | The tenant associated with this tenant blog | 
**state** | [**BlogPostState**](BlogPostState.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.blog_post import BlogPost

# TODO update the JSON string below
json = "{}"
# create an instance of BlogPost from a JSON string
blog_post_instance = BlogPost.from_json(json)
# print the JSON string representation of the object
print(BlogPost.to_json())

# convert the object into a dict
blog_post_dict = blog_post_instance.to_dict()
# create an instance of BlogPost from a dict
blog_post_from_dict = BlogPost.from_dict(blog_post_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


