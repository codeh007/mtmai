# BrowserConfig

浏览器配置(未完成)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**persistent** | **bool** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.browser_config import BrowserConfig

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserConfig from a JSON string
browser_config_instance = BrowserConfig.from_json(json)
# print the JSON string representation of the object
print(BrowserConfig.to_json())

# convert the object into a dict
browser_config_dict = browser_config_instance.to_dict()
# create an instance of BrowserConfig from a dict
browser_config_from_dict = BrowserConfig.from_dict(browser_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


