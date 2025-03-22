# CreateSiteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | site 标题 | 
**description** | **str** | site 描述 | 
**host** | **str** | 入站域名(指定绑定入站域名) | [optional] 

## Example

```python
from mtmai.clients.rest.models.create_site_request import CreateSiteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSiteRequest from a JSON string
create_site_request_instance = CreateSiteRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSiteRequest.to_json())

# convert the object into a dict
create_site_request_dict = create_site_request_instance.to_dict()
# create an instance of CreateSiteRequest from a dict
create_site_request_from_dict = CreateSiteRequest.from_dict(create_site_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


