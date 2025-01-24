# UpdateSiteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | site 标题 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.update_site_request import UpdateSiteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSiteRequest from a JSON string
update_site_request_instance = UpdateSiteRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSiteRequest.to_json())

# convert the object into a dict
update_site_request_dict = update_site_request_instance.to_dict()
# create an instance of UpdateSiteRequest from a dict
update_site_request_from_dict = UpdateSiteRequest.from_dict(update_site_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


