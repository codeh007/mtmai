# BrowserParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input** | **str** |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.browser_params import BrowserParams

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserParams from a JSON string
browser_params_instance = BrowserParams.from_json(json)
# print the JSON string representation of the object
print(BrowserParams.to_json())

# convert the object into a dict
browser_params_dict = browser_params_instance.to_dict()
# create an instance of BrowserParams from a dict
browser_params_from_dict = BrowserParams.from_dict(browser_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


