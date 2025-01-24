# RateLimitList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[RateLimit]**](RateLimit.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.rate_limit_list import RateLimitList

# TODO update the JSON string below
json = "{}"
# create an instance of RateLimitList from a JSON string
rate_limit_list_instance = RateLimitList.from_json(json)
# print the JSON string representation of the object
print(RateLimitList.to_json())

# convert the object into a dict
rate_limit_list_dict = rate_limit_list_instance.to_dict()
# create an instance of RateLimitList from a dict
rate_limit_list_from_dict = RateLimitList.from_dict(rate_limit_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


