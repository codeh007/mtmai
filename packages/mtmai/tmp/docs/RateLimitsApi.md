# mtmaisdk.clients.rest.RateLimitsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**rate_limit_list**](RateLimitsApi.md#rate_limit_list) | **GET** /api/v1/tenants/{tenant}/rate-limits | List rate limits


# **rate_limit_list**
> RateLimitList rate_limit_list(tenant, offset=offset, limit=limit, search=search, order_by_field=order_by_field, order_by_direction=order_by_direction)

List rate limits

Lists all rate limits for a tenant.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.rate_limit_list import RateLimitList
from mtmaisdk.clients.rest.models.rate_limit_order_by_direction import RateLimitOrderByDirection
from mtmaisdk.clients.rest.models.rate_limit_order_by_field import RateLimitOrderByField
from mtmaisdk.clients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmaisdk.clients.rest.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = mtmaisdk.clients.rest.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Configure Bearer authorization: bearerAuth
configuration = mtmaisdk.clients.rest.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with mtmaisdk.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmaisdk.clients.rest.RateLimitsApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)
    search = 'search_example' # str | The search query to filter for (optional)
    order_by_field = mtmaisdk.clients.rest.RateLimitOrderByField() # RateLimitOrderByField | What to order by (optional)
    order_by_direction = mtmaisdk.clients.rest.RateLimitOrderByDirection() # RateLimitOrderByDirection | The order direction (optional)

    try:
        # List rate limits
        api_response = await api_instance.rate_limit_list(tenant, offset=offset, limit=limit, search=search, order_by_field=order_by_field, order_by_direction=order_by_direction)
        print("The response of RateLimitsApi->rate_limit_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RateLimitsApi->rate_limit_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 
 **search** | **str**| The search query to filter for | [optional] 
 **order_by_field** | [**RateLimitOrderByField**](.md)| What to order by | [optional] 
 **order_by_direction** | [**RateLimitOrderByDirection**](.md)| The order direction | [optional] 

### Return type

[**RateLimitList**](RateLimitList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed the rate limits |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

