# BrowserUpdate


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
from mtmai.clients.rest.models.browser_update import BrowserUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserUpdate from a JSON string
browser_update_instance = BrowserUpdate.from_json(json)
# print the JSON string representation of the object
print(BrowserUpdate.to_json())

# convert the object into a dict
browser_update_dict = browser_update_instance.to_dict()
# create an instance of BrowserUpdate from a dict
browser_update_from_dict = BrowserUpdate.from_dict(browser_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


