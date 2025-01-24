# BlogPostState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | post title | [optional] 
**topic** | **str** | post topic | [optional] 
**outlines** | [**List[BlogPostStateOutlinesInner]**](BlogPostStateOutlinesInner.md) | post outlines | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.blog_post_state import BlogPostState

# TODO update the JSON string below
json = "{}"
# create an instance of BlogPostState from a JSON string
blog_post_state_instance = BlogPostState.from_json(json)
# print the JSON string representation of the object
print(BlogPostState.to_json())

# convert the object into a dict
blog_post_state_dict = blog_post_state_instance.to_dict()
# create an instance of BlogPostState from a dict
blog_post_state_from_dict = BlogPostState.from_dict(blog_post_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


