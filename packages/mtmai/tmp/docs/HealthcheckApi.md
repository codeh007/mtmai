# mtmai.gomtmclients.rest.HealthcheckApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**liveness_get**](HealthcheckApi.md#liveness_get) | **GET** /api/live | Get liveness
[**readiness_get**](HealthcheckApi.md#readiness_get) | **GET** /api/ready | Get readiness


# **liveness_get**
> liveness_get()

Get liveness

Gets the liveness status

### Example


```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmai.gomtmclients.rest.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with mtmai.gomtmclients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.gomtmclients.rest.HealthcheckApi(api_client)

    try:
        # Get liveness
        await api_instance.liveness_get()
    except Exception as e:
        print("Exception when calling HealthcheckApi->liveness_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Healthy |  -  |
**500** | Not liveness |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **readiness_get**
> readiness_get()

Get readiness

Gets the readiness status

### Example


```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = mtmai.gomtmclients.rest.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with mtmai.gomtmclients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.gomtmclients.rest.HealthcheckApi(api_client)

    try:
        # Get readiness
        await api_instance.readiness_get()
    except Exception as e:
        print("Exception when calling HealthcheckApi->readiness_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Healthy |  -  |
**500** | Not ready to accept traffic |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

