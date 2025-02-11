# mtmaisdk.clients.rest.PostsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_list**](PostsApi.md#post_list) | **GET** /api/v1/tenants/{tenant}/posts | 
[**post_list_public**](PostsApi.md#post_list_public) | **GET** /api/v1/posts/public | 


# **post_list**
> PostList post_list(tenant, site_id=site_id)



Get the posts for the site

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.post_list import PostList
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
    api_instance = mtmaisdk.clients.rest.PostsApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    site_id = 'site_id_example' # str | The site id (optional)

    try:
        api_response = await api_instance.post_list(tenant, site_id=site_id)
        print("The response of PostsApi->post_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->post_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **site_id** | **str**| The site id | [optional] 

### Return type

[**PostList**](PostList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_list_public**
> PostList post_list_public(site_id=site_id)



Get the posts for the site

### Example


```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.post_list import PostList
from mtmaisdk.clients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmaisdk.clients.rest.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with mtmaisdk.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmaisdk.clients.rest.PostsApi(api_client)
    site_id = 'site_id_example' # str | The site id (optional)

    try:
        api_response = await api_instance.post_list_public(site_id=site_id)
        print("The response of PostsApi->post_list_public:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->post_list_public: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **site_id** | **str**| The site id | [optional] 

### Return type

[**PostList**](PostList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

