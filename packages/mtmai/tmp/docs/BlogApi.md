# mtmai.clients.rest.BlogApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**blog_update**](BlogApi.md#blog_update) | **PATCH** /api/v1/tenants/{tenant}/blogs/{blog} | Update blog


# **blog_update**
> Blog blog_update(tenant, blog, update_blog_request)

Update blog

Update an existing blog

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.blog import Blog
from mtmai.clients.rest.models.update_blog_request import UpdateBlogRequest
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
    api_instance = mtmai.clients.rest.BlogApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    blog = 'blog_example' # str | The blog id
    update_blog_request = mtmai.clients.rest.UpdateBlogRequest() # UpdateBlogRequest | The tenant properties to update

    try:
        # Update blog
        api_response = await api_instance.blog_update(tenant, blog, update_blog_request)
        print("The response of BlogApi->blog_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BlogApi->blog_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **blog** | **str**| The blog id | 
 **update_blog_request** | [**UpdateBlogRequest**](UpdateBlogRequest.md)| The tenant properties to update | 

### Return type

[**Blog**](Blog.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the tenant |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

