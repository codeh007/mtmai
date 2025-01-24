# CreateSiteHostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**site_id** | **str** | 站点ID | 
**title** | **str** | site-host 标题 | 
**description** | **str** | site-host 描述 | 
**host** | **str** | 绑定域名 | 

## Example

```python
from mtmai.gomtmclients.rest.models.create_site_host_request import CreateSiteHostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSiteHostRequest from a JSON string
create_site_host_request_instance = CreateSiteHostRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSiteHostRequest.to_json())

# convert the object into a dict
create_site_host_request_dict = create_site_host_request_instance.to_dict()
# create an instance of CreateSiteHostRequest from a dict
create_site_host_request_from_dict = CreateSiteHostRequest.from_dict(create_site_host_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


