# mtmai.clients.rest.MtmaiApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**mtmai_bloggenconfig**](MtmaiApi.md#mtmai_bloggenconfig) | **GET** /api/v1/mtmai/bloggenconfig | 获取博客生成配置
[**mtmai_worker_config**](MtmaiApi.md#mtmai_worker_config) | **GET** /api/v1/mtmai/worker_config | 


# **mtmai_bloggenconfig**
> BlogGenConfig mtmai_bloggenconfig()

获取博客生成配置

获取博客生成配置

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.blog_gen_config import BlogGenConfig
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
    api_instance = mtmai.clients.rest.MtmaiApi(api_client)

    try:
        # 获取博客生成配置
        api_response = await api_instance.mtmai_bloggenconfig()
        print("The response of MtmaiApi->mtmai_bloggenconfig:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MtmaiApi->mtmai_bloggenconfig: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BlogGenConfig**](BlogGenConfig.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 博客生成配置 |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mtmai_worker_config**
> MtmaiWorkerConfig200Response mtmai_worker_config()



### Example


```python
import mtmai.clients.rest
from mtmai.clients.rest.models.mtmai_worker_config200_response import MtmaiWorkerConfig200Response
from mtmai.clients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmai.clients.rest.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.MtmaiApi(api_client)

    try:
        api_response = await api_instance.mtmai_worker_config()
        print("The response of MtmaiApi->mtmai_worker_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MtmaiApi->mtmai_worker_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**MtmaiWorkerConfig200Response**](MtmaiWorkerConfig200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

