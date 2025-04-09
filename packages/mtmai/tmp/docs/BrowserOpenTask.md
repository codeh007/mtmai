# BrowserOpenTask

打开浏览器备用,一般用于调试目的Open a browser and navigate to a URL.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.browser_open_task import BrowserOpenTask

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserOpenTask from a JSON string
browser_open_task_instance = BrowserOpenTask.from_json(json)
# print the JSON string representation of the object
print(BrowserOpenTask.to_json())

# convert the object into a dict
browser_open_task_dict = browser_open_task_instance.to_dict()
# create an instance of BrowserOpenTask from a dict
browser_open_task_from_dict = BrowserOpenTask.from_dict(browser_open_task_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


