# ProxyList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Proxy]**](Proxy.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.proxy_list import ProxyList

# TODO update the JSON string below
json = "{}"
# create an instance of ProxyList from a JSON string
proxy_list_instance = ProxyList.from_json(json)
# print the JSON string representation of the object
print(ProxyList.to_json())

# convert the object into a dict
proxy_list_dict = proxy_list_instance.to_dict()
# create an instance of ProxyList from a dict
proxy_list_from_dict = ProxyList.from_dict(proxy_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


