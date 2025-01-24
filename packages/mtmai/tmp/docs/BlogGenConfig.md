# BlogGenConfig

博客站点生成基本配置

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | 站点名称. | 
**description** | **str** | 博客站点介绍. | 
**seo_keywords** | **str** | 站点关键字列表 | [optional] 
**day_publish_count_hint** | **float** | 站点建议日更帖子数量 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.blog_gen_config import BlogGenConfig

# TODO update the JSON string below
json = "{}"
# create an instance of BlogGenConfig from a JSON string
blog_gen_config_instance = BlogGenConfig.from_json(json)
# print the JSON string representation of the object
print(BlogGenConfig.to_json())

# convert the object into a dict
blog_gen_config_dict = blog_gen_config_instance.to_dict()
# create an instance of BlogGenConfig from a dict
blog_gen_config_from_dict = BlogGenConfig.from_dict(blog_gen_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


