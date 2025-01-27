# CanvasGraphParamsAction

节点运行

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | 动作 | [optional] 
**input** | **object** | 输入 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.canvas_graph_params_action import CanvasGraphParamsAction

# TODO update the JSON string below
json = "{}"
# create an instance of CanvasGraphParamsAction from a JSON string
canvas_graph_params_action_instance = CanvasGraphParamsAction.from_json(json)
# print the JSON string representation of the object
print(CanvasGraphParamsAction.to_json())

# convert the object into a dict
canvas_graph_params_action_dict = canvas_graph_params_action_instance.to_dict()
# create an instance of CanvasGraphParamsAction from a dict
canvas_graph_params_action_from_dict = CanvasGraphParamsAction.from_dict(canvas_graph_params_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


