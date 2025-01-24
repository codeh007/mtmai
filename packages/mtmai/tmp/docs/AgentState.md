# AgentState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**thread_id** | **str** | 线程ID | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | 
**name** | **str** | 节点名称 | 
**description** | **str** | 描述 | 
**blog_task_state** | [**BlogTaskState**](BlogTaskState.md) | 关联的上级博客生成任务 | [optional] 
**topic** | **str** | 当前关联的主题 | 
**prompt** | **str** | 关键提示语 | [optional] 
**title** | **str** | 文章主标题 | [optional] 
**sub_title** | **str** | 文章副标题 | [optional] 
**oulines** | [**List[GenArticleStateAllOfOulines]**](GenArticleStateAllOfOulines.md) | 文章大纲列表 | [optional] 
**llm** | [**LlmConfig**](LlmConfig.md) |  | [optional] 
**blog_description** | **str** | 博客站点功能定位描述 | 
**blog_keywords** | **List[str]** | 博客的SEO关键字 | 
**cur_topic_to_gen** | **str** | 当前生成文章使用的主题 | [optional] 
**cur_article_state** | [**GenArticleState**](GenArticleState.md) | 当前正在生成的文章 | [optional] 
**step_description** | **str** | 当前步骤描述 | [optional] 
**running_state** | **str** | 运行状态 | [optional] 
**day_publishd_count** | **float** | 已经完成的日更天子数量 | [default to 0]
**day_publish_count_hint** | **float** | 建议日更数 | [default to 10]
**channel** | [**PostizChannel**](PostizChannel.md) |  | [optional] 
**id** | **str** | 消息ID | 
**content** | **str** | 消息内容 | 
**input** | **str** | 节点输入 | 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_state import AgentState

# TODO update the JSON string below
json = "{}"
# create an instance of AgentState from a JSON string
agent_state_instance = AgentState.from_json(json)
# print the JSON string representation of the object
print(AgentState.to_json())

# convert the object into a dict
agent_state_dict = agent_state_instance.to_dict()
# create an instance of AgentState from a dict
agent_state_from_dict = AgentState.from_dict(agent_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


