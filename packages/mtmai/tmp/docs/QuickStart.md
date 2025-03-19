# QuickStart


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**icon** | **str** | 图标 | [optional] 
**com_id** | **str** | 组件ID (团队ID) | [optional] 
**title** | **str** | 摘要 | [optional] 
**content** | **str** | 提交跟 agent 的内容 | 
**cn** | **str** | html class name | [optional] 

## Example

```python
from mtmai.clients.rest.models.quick_start import QuickStart

# TODO update the JSON string below
json = "{}"
# create an instance of QuickStart from a JSON string
quick_start_instance = QuickStart.from_json(json)
# print the JSON string representation of the object
print(QuickStart.to_json())

# convert the object into a dict
quick_start_dict = quick_start_instance.to_dict()
# create an instance of QuickStart from a dict
quick_start_from_dict = QuickStart.from_dict(quick_start_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


