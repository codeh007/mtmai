# BlogConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**day_publish_count** | **int** | The number of posts to publish per day. | [optional] 
**description** | **str** | The description of the blog. | [optional] 

## Example

```python
from mtmai.clients.rest.models.blog_config import BlogConfig

# TODO update the JSON string below
json = "{}"
# create an instance of BlogConfig from a JSON string
blog_config_instance = BlogConfig.from_json(json)
# print the JSON string representation of the object
print(BlogConfig.to_json())

# convert the object into a dict
blog_config_dict = blog_config_instance.to_dict()
# create an instance of BlogConfig from a dict
blog_config_from_dict = BlogConfig.from_dict(blog_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


