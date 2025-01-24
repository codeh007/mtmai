# BlogPostStateOutlinesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | post outline title | [optional] 
**content** | **str** | post outline content | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.blog_post_state_outlines_inner import BlogPostStateOutlinesInner

# TODO update the JSON string below
json = "{}"
# create an instance of BlogPostStateOutlinesInner from a JSON string
blog_post_state_outlines_inner_instance = BlogPostStateOutlinesInner.from_json(json)
# print the JSON string representation of the object
print(BlogPostStateOutlinesInner.to_json())

# convert the object into a dict
blog_post_state_outlines_inner_dict = blog_post_state_outlines_inner_instance.to_dict()
# create an instance of BlogPostStateOutlinesInner from a dict
blog_post_state_outlines_inner_from_dict = BlogPostStateOutlinesInner.from_dict(blog_post_state_outlines_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


