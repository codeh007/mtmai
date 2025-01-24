# DashSidebarItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | 名称 | 
**url** | **str** | url 例如/login | 
**icon** | **str** | 图标 | [optional] 
**default_expanded** | **bool** | 默认展开 | [optional] 
**admin_only** | **bool** | 只允许超级管理员查看 | [optional] 
**children** | [**List[DashSidebarItem]**](DashSidebarItem.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.dash_sidebar_item import DashSidebarItem

# TODO update the JSON string below
json = "{}"
# create an instance of DashSidebarItem from a JSON string
dash_sidebar_item_instance = DashSidebarItem.from_json(json)
# print the JSON string representation of the object
print(DashSidebarItem.to_json())

# convert the object into a dict
dash_sidebar_item_dict = dash_sidebar_item_instance.to_dict()
# create an instance of DashSidebarItem from a dict
dash_sidebar_item_from_dict = DashSidebarItem.from_dict(dash_sidebar_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


