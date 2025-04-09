# BrowserTask

浏览器(browser use)任务

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.browser_task import BrowserTask

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserTask from a JSON string
browser_task_instance = BrowserTask.from_json(json)
# print the JSON string representation of the object
print(BrowserTask.to_json())

# convert the object into a dict
browser_task_dict = browser_task_instance.to_dict()
# create an instance of BrowserTask from a dict
browser_task_from_dict = BrowserTask.from_dict(browser_task_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


