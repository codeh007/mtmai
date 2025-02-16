# ProxyUpdate


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
from mtmai.clients.rest.models.proxy_update import ProxyUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ProxyUpdate from a JSON string
proxy_update_instance = ProxyUpdate.from_json(json)
# print the JSON string representation of the object
print(ProxyUpdate.to_json())

# convert the object into a dict
proxy_update_dict = proxy_update_instance.to_dict()
# create an instance of ProxyUpdate from a dict
proxy_update_from_dict = ProxyUpdate.from_dict(proxy_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


