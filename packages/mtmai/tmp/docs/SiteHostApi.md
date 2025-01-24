# mtmai.gomtmclients.rest.SiteHostApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**site_host_create**](SiteHostApi.md#site_host_create) | **POST** /api/v1/tenants/{tenant}/site-hosts | 
[**site_host_get**](SiteHostApi.md#site_host_get) | **GET** /api/v1/tenants/{tenant}/site-hosts/{host} | 
[**site_host_list**](SiteHostApi.md#site_host_list) | **GET** /api/v1/tenants/{tenant}/site-hosts | 


# **site_host_create**
> SiteHost site_host_create(tenant, create_site_host_request)



create site-host

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.create_site_host_request import CreateSiteHostRequest
from mtmai.gomtmclients.rest.models.site_host import SiteHost
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
    api_instance = mtmai.gomtmclients.rest.SiteHostApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    create_site_host_request = mtmai.gomtmclients.rest.CreateSiteHostRequest() # CreateSiteHostRequest | 创建agentnode

    try:
        api_response = await api_instance.site_host_create(tenant, create_site_host_request)
        print("The response of SiteHostApi->site_host_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SiteHostApi->site_host_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **create_site_host_request** | [**CreateSiteHostRequest**](CreateSiteHostRequest.md)| 创建agentnode | 

### Return type

[**SiteHost**](SiteHost.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **site_host_get**
> SiteHost site_host_get(tenant, host)



Get the site-host for the tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.site_host import SiteHost
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
    api_instance = mtmai.gomtmclients.rest.SiteHostApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    host = 'host_example' # str | The site-host id

    try:
        api_response = await api_instance.site_host_get(tenant, host)
        print("The response of SiteHostApi->site_host_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SiteHostApi->site_host_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **host** | **str**| The site-host id | 

### Return type

[**SiteHost**](SiteHost.md)

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

# **site_host_list**
> SiteHostList site_host_list(tenant, offset=offset, host=host, site_id=site_id)



Get the site-hosts for the tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.site_host_list import SiteHostList
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
    api_instance = mtmai.gomtmclients.rest.SiteHostApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    offset = 56 # int | The number to skip (optional)
    host = 'host_example' # str | The host name (optional)
    site_id = 'site_id_example' # str | The site id (optional)

    try:
        api_response = await api_instance.site_host_list(tenant, offset=offset, host=host, site_id=site_id)
        print("The response of SiteHostApi->site_host_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SiteHostApi->site_host_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **offset** | **int**| The number to skip | [optional] 
 **host** | **str**| The host name | [optional] 
 **site_id** | **str**| The site id | [optional] 

### Return type

[**SiteHostList**](SiteHostList.md)

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

