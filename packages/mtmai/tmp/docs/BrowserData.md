# BrowserData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**cookies** | **str** |  | [optional] 
**session** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.browser_data import BrowserData

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserData from a JSON string
browser_data_instance = BrowserData.from_json(json)
# print the JSON string representation of the object
print(BrowserData.to_json())

# convert the object into a dict
browser_data_dict = browser_data_instance.to_dict()
# create an instance of BrowserData from a dict
browser_data_from_dict = BrowserData.from_dict(browser_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


