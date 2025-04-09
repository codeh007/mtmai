# ListSNSIntegrations


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | 
**rows** | [**List[SNSIntegration]**](SNSIntegration.md) |  | 

## Example

```python
from mtmai.clients.rest.models.list_sns_integrations import ListSNSIntegrations

# TODO update the JSON string below
json = "{}"
# create an instance of ListSNSIntegrations from a JSON string
list_sns_integrations_instance = ListSNSIntegrations.from_json(json)
# print the JSON string representation of the object
print(ListSNSIntegrations.to_json())

# convert the object into a dict
list_sns_integrations_dict = list_sns_integrations_instance.to_dict()
# create an instance of ListSNSIntegrations from a dict
list_sns_integrations_from_dict = ListSNSIntegrations.from_dict(list_sns_integrations_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


