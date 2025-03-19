# TenantComponentConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_openai_api_key** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.tenant_component_config import TenantComponentConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TenantComponentConfig from a JSON string
tenant_component_config_instance = TenantComponentConfig.from_json(json)
# print the JSON string representation of the object
print(TenantComponentConfig.to_json())

# convert the object into a dict
tenant_component_config_dict = tenant_component_config_instance.to_dict()
# create an instance of TenantComponentConfig from a dict
tenant_component_config_from_dict = TenantComponentConfig.from_dict(tenant_component_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


