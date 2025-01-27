# AgentNodeRunInputParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_stream** | **bool** |  | 
**thread_id** | **str** |  | 
**input** | **str** |  | 
**step_limit** | **float** | 步骤限制(没用上) | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 
**action** | [**CanvasGraphParamsAction**](CanvasGraphParamsAction.md) |  | [optional] 
**language** | **str** | 语言 | [optional] 
**custom_quick_action_id** | **str** | 自定义快速动作ID | [optional] 
**artifact_id** | **str** | 工件ID | [optional] 
**fix_bugs** | **bool** | 是否修复bug | [optional] 
**highlighted_code** | [**CodeHighlight**](.md) |  | [optional] 
**highlighted_text** | [**TextHighlight**](.md) |  | [optional] 
**regenerate_with_emojis** | **bool** | 是否使用表情符号重新生成 | [optional] 
**reading_level** | [**ReadingLevelOptions**](ReadingLevelOptions.md) | 阅读级别 | [optional] 
**artifact_length** | [**ArtifactLengthOptions**](ArtifactLengthOptions.md) | 工具内容长度,(文章,代码内容长度) | [optional] 
**artifact** | [**ArtifactV3**](.md) |  | [optional] 
**add_comments** | **bool** |  | [optional] 
**add_logs** | **bool** |  | [optional] 
**port_language** | [**ProgrammingLanguageOptions**](ProgrammingLanguageOptions.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.agent_node_run_input_params import AgentNodeRunInputParams

# TODO update the JSON string below
json = "{}"
# create an instance of AgentNodeRunInputParams from a JSON string
agent_node_run_input_params_instance = AgentNodeRunInputParams.from_json(json)
# print the JSON string representation of the object
print(AgentNodeRunInputParams.to_json())

# convert the object into a dict
agent_node_run_input_params_dict = agent_node_run_input_params_instance.to_dict()
# create an instance of AgentNodeRunInputParams from a dict
agent_node_run_input_params_from_dict = AgentNodeRunInputParams.from_dict(agent_node_run_input_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


