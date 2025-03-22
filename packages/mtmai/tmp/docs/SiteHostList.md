# SiteHostList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[SiteHost]**](SiteHost.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.site_host_list import SiteHostList

# TODO update the JSON string below
json = "{}"
# create an instance of SiteHostList from a JSON string
site_host_list_instance = SiteHostList.from_json(json)
# print the JSON string representation of the object
print(SiteHostList.to_json())

# convert the object into a dict
site_host_list_dict = site_host_list_instance.to_dict()
# create an instance of SiteHostList from a dict
site_host_list_from_dict = SiteHostList.from_dict(site_host_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


