# NodeRunAction

节点运行

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | 动作 | [optional] 
**input** | **object** | 输入 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.node_run_action import NodeRunAction

# TODO update the JSON string below
json = "{}"
# create an instance of NodeRunAction from a JSON string
node_run_action_instance = NodeRunAction.from_json(json)
# print the JSON string representation of the object
print(NodeRunAction.to_json())

# convert the object into a dict
node_run_action_dict = node_run_action_instance.to_dict()
# create an instance of NodeRunAction from a dict
node_run_action_from_dict = NodeRunAction.from_dict(node_run_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


