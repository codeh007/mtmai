# SiteHost

site-host

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**title** | **str** | site-host 标题 | 
**description** | **str** | site-host 描述 | 
**host** | **str** | 绑定域名 | 

## Example

```python
from mtmaisdk.clients.rest.models.site_host import SiteHost

# TODO update the JSON string below
json = "{}"
# create an instance of SiteHost from a JSON string
site_host_instance = SiteHost.from_json(json)
# print the JSON string representation of the object
print(SiteHost.to_json())

# convert the object into a dict
site_host_dict = site_host_instance.to_dict()
# create an instance of SiteHost from a dict
site_host_from_dict = SiteHost.from_dict(site_host_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


