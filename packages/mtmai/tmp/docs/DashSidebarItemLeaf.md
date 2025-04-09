# DashSidebarItemLeaf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | 名称 | 
**url** | **str** | url 例如/login | 
**icon** | **str** | 图标 | [optional] 
**admin_only** | **bool** | 只允许超级管理员查看 | [optional] 

## Example

```python
from mtmai.clients.rest.models.dash_sidebar_item_leaf import DashSidebarItemLeaf

# TODO update the JSON string below
json = "{}"
# create an instance of DashSidebarItemLeaf from a JSON string
dash_sidebar_item_leaf_instance = DashSidebarItemLeaf.from_json(json)
# print the JSON string representation of the object
print(DashSidebarItemLeaf.to_json())

# convert the object into a dict
dash_sidebar_item_leaf_dict = dash_sidebar_item_leaf_instance.to_dict()
# create an instance of DashSidebarItemLeaf from a dict
dash_sidebar_item_leaf_from_dict = DashSidebarItemLeaf.from_dict(dash_sidebar_item_leaf_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


