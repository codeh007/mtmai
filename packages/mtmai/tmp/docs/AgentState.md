# AgentState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
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
**channel** | [**PostizChannel**](PostizChannel.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.agent_state import AgentState

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


