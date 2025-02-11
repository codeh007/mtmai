# mtmaisdk.clients.rest.MetadataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cloud_metadata_get**](MetadataApi.md#cloud_metadata_get) | **GET** /api/v1/cloud/metadata | Get cloud metadata
[**metadata_get**](MetadataApi.md#metadata_get) | **GET** /api/v1/meta | Get metadata
[**metadata_list_integrations**](MetadataApi.md#metadata_list_integrations) | **GET** /api/v1/meta/integrations | List integrations


# **cloud_metadata_get**
> APIErrors cloud_metadata_get()

Get cloud metadata

Gets metadata for the Hatchet cloud instance

### Example


```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.api_errors import APIErrors
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
    api_instance = mtmaisdk.clients.rest.MetadataApi(api_client)

    try:
        # Get cloud metadata
        api_response = await api_instance.cloud_metadata_get()
        print("The response of MetadataApi->cloud_metadata_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetadataApi->cloud_metadata_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**APIErrors**](APIErrors.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cloud unavailable |  -  |
**400** | A malformed or bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_get**
> APIMeta metadata_get()

Get metadata

Gets metadata for the Hatchet instance

### Example


```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.api_meta import APIMeta
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
    api_instance = mtmaisdk.clients.rest.MetadataApi(api_client)

    try:
        # Get metadata
        api_response = await api_instance.metadata_get()
        print("The response of MetadataApi->metadata_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetadataApi->metadata_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**APIMeta**](APIMeta.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the metadata |  -  |
**400** | A malformed or bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_list_integrations**
> List[APIMetaIntegration] metadata_list_integrations()

List integrations

List all integrations

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.api_meta_integration import APIMetaIntegration
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
    api_instance = mtmaisdk.clients.rest.MetadataApi(api_client)

    try:
        # List integrations
        api_response = await api_instance.metadata_list_integrations()
        print("The response of MetadataApi->metadata_list_integrations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetadataApi->metadata_list_integrations: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[APIMetaIntegration]**](APIMetaIntegration.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the list of integrations |  -  |
**400** | A malformed or bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

