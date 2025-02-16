# mtmai.clients.rest.AgStateApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ag_state_upsert**](AgStateApi.md#ag_state_upsert) | **PATCH** /api/v1/tenants/{tenant}/agStates | 


# **ag_state_upsert**
> AgState ag_state_upsert(tenant, ag_state_upsert)



Upsert an agState

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.ag_state import AgState
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmai.clients.rest.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = mtmai.clients.rest.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Configure Bearer authorization: bearerAuth
configuration = mtmai.clients.rest.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.AgStateApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    ag_state_upsert = mtmai.clients.rest.AgStateUpsert() # AgStateUpsert | The model properties to update

    try:
        api_response = await api_instance.ag_state_upsert(tenant, ag_state_upsert)
        print("The response of AgStateApi->ag_state_upsert:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgStateApi->ag_state_upsert: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **ag_state_upsert** | [**AgStateUpsert**](AgStateUpsert.md)| The model properties to update | 

### Return type

[**AgState**](AgState.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the AgState |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

