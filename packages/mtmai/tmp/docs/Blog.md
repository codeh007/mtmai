# Blog


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**tenant** | [**Tenant**](Tenant.md) | The tenant associated with this tenant blog. | [optional] 
**config** | [**BlogConfig**](BlogConfig.md) |  | [optional] 
**status** | **str** | The status of the blog. | [optional] 
**enabled** | **bool** | Whether the blog is enabled. | [optional] 
**slug** | **str** | The slug of the blog. | [optional] 

## Example

```python
from mtmai.clients.rest.models.blog import Blog

# TODO update the JSON string below
json = "{}"
# create an instance of Blog from a JSON string
blog_instance = Blog.from_json(json)
# print the JSON string representation of the object
print(Blog.to_json())

# convert the object into a dict
blog_dict = blog_instance.to_dict()
# create an instance of Blog from a dict
blog_from_dict = Blog.from_dict(blog_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


