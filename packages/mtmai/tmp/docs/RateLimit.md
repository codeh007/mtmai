# RateLimit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The key for the rate limit. | 
**tenant_id** | **str** | The ID of the tenant associated with this rate limit. | 
**limit_value** | **int** | The maximum number of requests allowed within the window. | 
**value** | **int** | The current number of requests made within the window. | 
**window** | **str** | The window of time in which the limitValue is enforced. | 
**last_refill** | **datetime** | The last time the rate limit was refilled. | 

## Example

```python
from mtmai.clients.rest.models.rate_limit import RateLimit

# TODO update the JSON string below
json = "{}"
# create an instance of RateLimit from a JSON string
rate_limit_instance = RateLimit.from_json(json)
# print the JSON string representation of the object
print(RateLimit.to_json())

# convert the object into a dict
rate_limit_dict = rate_limit_instance.to_dict()
# create an instance of RateLimit from a dict
rate_limit_from_dict = RateLimit.from_dict(rate_limit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


