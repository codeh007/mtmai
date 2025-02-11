# SiteList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Site]**](Site.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.site_list import SiteList

# TODO update the JSON string below
json = "{}"
# create an instance of SiteList from a JSON string
site_list_instance = SiteList.from_json(json)
# print the JSON string representation of the object
print(SiteList.to_json())

# convert the object into a dict
site_list_dict = site_list_instance.to_dict()
# create an instance of SiteList from a dict
site_list_from_dict = SiteList.from_dict(site_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


