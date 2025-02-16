# mtmai.clients.rest.FrontendApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**frontend_get_config**](FrontendApi.md#frontend_get_config) | **GET** /api/v1/frontend/config | 
[**frontend_get_siderbar**](FrontendApi.md#frontend_get_siderbar) | **GET** /api/v1/frontend/siderbar | 


# **frontend_get_config**
> FrontendConfig frontend_get_config()



### Example


```python
import mtmai.clients.rest
from mtmai.clients.rest.models.frontend_config import FrontendConfig
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
    api_instance = mtmai.clients.rest.FrontendApi(api_client)

    try:
        api_response = await api_instance.frontend_get_config()
        print("The response of FrontendApi->frontend_get_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FrontendApi->frontend_get_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FrontendConfig**](FrontendConfig.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | frontend core config |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **frontend_get_siderbar**
> SiderbarConfig frontend_get_siderbar()



### Example


```python
import mtmai.clients.rest
from mtmai.clients.rest.models.siderbar_config import SiderbarConfig
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
    api_instance = mtmai.clients.rest.FrontendApi(api_client)

    try:
        api_response = await api_instance.frontend_get_siderbar()
        print("The response of FrontendApi->frontend_get_siderbar:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FrontendApi->frontend_get_siderbar: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SiderbarConfig**](SiderbarConfig.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | frontend siderbar config |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

