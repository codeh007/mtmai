# AgentRun200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**workflow_run_id** | **str** |  | [optional] 
**id** | **str** | 消息ID | 
**content** | **str** | 消息内容 | 
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**thread_id** | **str** | 线程ID | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | 
**name** | **str** | 名称 | 
**description** | **str** | 描述 | 
**topic** | **str** | 当前关联的主题 | 
**prompt** | **str** | 关键提示语 | [optional] 
**title** | **str** | 文章主标题 | [optional] 
**sub_title** | **str** | 文章副标题 | [optional] 
**oulines** | [**List[GenArticleStateAllOfOulines]**](GenArticleStateAllOfOulines.md) | 文章大纲列表 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.agent_run200_response import AgentRun200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentRun200Response from a JSON string
agent_run200_response_instance = AgentRun200Response.from_json(json)
# print the JSON string representation of the object
print(AgentRun200Response.to_json())

# convert the object into a dict
agent_run200_response_dict = agent_run200_response_instance.to_dict()
# create an instance of AgentRun200Response from a dict
agent_run200_response_from_dict = AgentRun200Response.from_dict(agent_run200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


