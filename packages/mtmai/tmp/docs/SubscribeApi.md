# mtmaisdk.clients.rest.SubscribeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**subscribe_subscribe**](SubscribeApi.md#subscribe_subscribe) | **POST** /api/v1/tenants/{tenant}/subscribe | 订阅消息接口


# **subscribe_subscribe**
> str subscribe_subscribe(tenant, subscribe_request=subscribe_request)

订阅消息接口

Subscribe to workflow run events

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.subscribe_request import SubscribeRequest
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
    api_instance = mtmaisdk.clients.rest.SubscribeApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    subscribe_request = mtmaisdk.clients.rest.SubscribeRequest() # SubscribeRequest |  (optional)

    try:
        # 订阅消息接口
        api_response = await api_instance.subscribe_subscribe(tenant, subscribe_request=subscribe_request)
        print("The response of SubscribeApi->subscribe_subscribe:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SubscribeApi->subscribe_subscribe: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **subscribe_request** | [**SubscribeRequest**](SubscribeRequest.md)|  | [optional] 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/event-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | chat 聊天应用 |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

