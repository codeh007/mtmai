# ListAPITokensResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[APIToken]**](APIToken.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.list_api_tokens_response import ListAPITokensResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListAPITokensResponse from a JSON string
list_api_tokens_response_instance = ListAPITokensResponse.from_json(json)
# print the JSON string representation of the object
print(ListAPITokensResponse.to_json())

# convert the object into a dict
list_api_tokens_response_dict = list_api_tokens_response_instance.to_dict()
# create an instance of ListAPITokensResponse from a dict
list_api_tokens_response_from_dict = ListAPITokensResponse.from_dict(list_api_tokens_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


