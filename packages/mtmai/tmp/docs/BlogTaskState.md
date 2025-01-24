# BlogTaskState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**thread_id** | **str** | 线程ID | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | 
**llm** | [**LlmConfig**](LlmConfig.md) |  | [optional] 
**prompt** | **str** | 关键提示语 | [optional] 
**blog_description** | **str** | 博客站点功能定位描述 | 
**blog_keywords** | **List[str]** | 博客的SEO关键字 | 
**cur_topic_to_gen** | **str** | 当前生成文章使用的主题 | [optional] 
**cur_article_state** | [**GenArticleState**](GenArticleState.md) | 当前正在生成的文章 | [optional] 
**step_description** | **str** | 当前步骤描述 | [optional] 
**running_state** | **str** | 运行状态 | [optional] 
**day_publishd_count** | **float** | 已经完成的日更天子数量 | [default to 0]
**day_publish_count_hint** | **float** | 建议日更数 | [default to 10]

## Example

```python
from mtmai.gomtmclients.rest.models.blog_task_state import BlogTaskState

# TODO update the JSON string below
json = "{}"
# create an instance of BlogTaskState from a JSON string
blog_task_state_instance = BlogTaskState.from_json(json)
# print the JSON string representation of the object
print(BlogTaskState.to_json())

# convert the object into a dict
blog_task_state_dict = blog_task_state_instance.to_dict()
# create an instance of BlogTaskState from a dict
blog_task_state_from_dict = BlogTaskState.from_dict(blog_task_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


