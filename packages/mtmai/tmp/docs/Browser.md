# Browser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**url** | **str** |  | 
**login_url** | **str** |  | [optional] 
**properties** | **object** |  | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.browser import Browser

# TODO update the JSON string below
json = "{}"
# create an instance of Browser from a JSON string
browser_instance = Browser.from_json(json)
# print the JSON string representation of the object
print(Browser.to_json())

# convert the object into a dict
browser_dict = browser_instance.to_dict()
# create an instance of Browser from a dict
browser_from_dict = Browser.from_dict(browser_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


