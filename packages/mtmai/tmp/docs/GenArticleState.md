# GenArticleState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**thread_id** | **str** | 线程ID | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | 
**blog_task_state** | [**BlogTaskState**](BlogTaskState.md) | 关联的上级博客生成任务 | [optional] 
**topic** | **str** | 当前关联的主题 | 
**prompt** | **str** | 关键提示语 | [optional] 
**title** | **str** | 文章主标题 | [optional] 
**sub_title** | **str** | 文章副标题 | [optional] 
**oulines** | [**List[GenArticleStateAllOfOulines]**](GenArticleStateAllOfOulines.md) | 文章大纲列表 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.gen_article_state import GenArticleState

# TODO update the JSON string below
json = "{}"
# create an instance of GenArticleState from a JSON string
gen_article_state_instance = GenArticleState.from_json(json)
# print the JSON string representation of the object
print(GenArticleState.to_json())

# convert the object into a dict
gen_article_state_dict = gen_article_state_instance.to_dict()
# create an instance of GenArticleState from a dict
gen_article_state_from_dict = GenArticleState.from_dict(gen_article_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


