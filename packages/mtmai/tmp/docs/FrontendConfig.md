# FrontendConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cookie_access_token** | **str** | Cookie access token | 
**dash_path** | **str** | Dashboard path | 
**hot_key_debug** | **str** | Hot key debug | 
**default_tenant_access_token** | **str** | 实验性质，默认租户的access token | 

## Example

```python
from mtmai.clients.rest.models.frontend_config import FrontendConfig

# TODO update the JSON string below
json = "{}"
# create an instance of FrontendConfig from a JSON string
frontend_config_instance = FrontendConfig.from_json(json)
# print the JSON string representation of the object
print(FrontendConfig.to_json())

# convert the object into a dict
frontend_config_dict = frontend_config_instance.to_dict()
# create an instance of FrontendConfig from a dict
frontend_config_from_dict = FrontendConfig.from_dict(frontend_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


