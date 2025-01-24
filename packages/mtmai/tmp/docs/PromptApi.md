# mtmai.gomtmclients.rest.PromptApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**prompt_get**](PromptApi.md#prompt_get) | **GET** /api/v1/tenants/{tenant}/prompts/{prompt} | 获取单个提示词
[**prompt_list**](PromptApi.md#prompt_list) | **GET** /api/v1/tenants/{tenant}/prompts | 提示词列表


# **prompt_get**
> str prompt_get(tenant, prompt)

获取单个提示词

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmai.gomtmclients.rest.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = mtmai.gomtmclients.rest.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Configure Bearer authorization: bearerAuth
configuration = mtmai.gomtmclients.rest.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with mtmai.gomtmclients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.gomtmclients.rest.PromptApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    prompt = 'prompt_example' # str | The prompt id

    try:
        # 获取单个提示词
        api_response = await api_instance.prompt_get(tenant, prompt)
        print("The response of PromptApi->prompt_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptApi->prompt_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **prompt** | **str**| The prompt id | 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/markdown, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 获取单个提示词 |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | A malformed or bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prompt_list**
> PromptList prompt_list(tenant)

提示词列表

Get the blogs for the tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.prompt_list import PromptList
from mtmai.gomtmclients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmai.gomtmclients.rest.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = mtmai.gomtmclients.rest.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Configure Bearer authorization: bearerAuth
configuration = mtmai.gomtmclients.rest.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with mtmai.gomtmclients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.gomtmclients.rest.PromptApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # 提示词列表
        api_response = await api_instance.prompt_list(tenant)
        print("The response of PromptApi->prompt_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptApi->prompt_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

[**PromptList**](PromptList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 提示词列表 |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

