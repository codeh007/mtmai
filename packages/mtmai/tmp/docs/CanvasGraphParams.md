# CanvasGraphParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**step_limit** | **float** | 步骤限制(没用上) | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 
**action** | [**NodeRunAction**](NodeRunAction.md) |  | [optional] 
**language** | **str** | 语言 | [optional] 
**custom_quick_action_id** | **str** | 自定义快速动作ID | [optional] 
**artifact_id** | **str** | 工件ID | [optional] 
**fix_bugs** | **bool** | 是否修复bug | [optional] 
**highlighted_code** | [**CodeHighlight**](CodeHighlight.md) |  | [optional] 
**highlighted_text** | [**TextHighlight**](TextHighlight.md) |  | [optional] 
**regenerate_with_emojis** | **bool** | 是否使用表情符号重新生成 | [optional] 
**reading_level** | [**ReadingLevelOptions**](ReadingLevelOptions.md) | 阅读级别 | [optional] 
**artifact_length** | [**ArtifactLengthOptions**](ArtifactLengthOptions.md) | 工具内容长度,(文章,代码内容长度) | [optional] 
**artifact** | [**ArtifactV3**](ArtifactV3.md) |  | [optional] 
**add_comments** | **bool** |  | [optional] 
**add_logs** | **bool** |  | [optional] 
**port_language** | [**ProgrammingLanguageOptions**](ProgrammingLanguageOptions.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.canvas_graph_params import CanvasGraphParams

# TODO update the JSON string below
json = "{}"
# create an instance of CanvasGraphParams from a JSON string
canvas_graph_params_instance = CanvasGraphParams.from_json(json)
# print the JSON string representation of the object
print(CanvasGraphParams.to_json())

# convert the object into a dict
canvas_graph_params_dict = canvas_graph_params_instance.to_dict()
# create an instance of CanvasGraphParams from a dict
canvas_graph_params_from_dict = CanvasGraphParams.from_dict(canvas_graph_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


