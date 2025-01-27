# mtmaisdk.clients.rest.GithubApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sns_update**](GithubApi.md#sns_update) | **POST** /api/v1/sns/{tenant}/{event} | Github app tenant webhook


# **sns_update**
> sns_update(tenant, event)

Github app tenant webhook

SNS event

### Example


```python
import mtmaisdk.clients.rest
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
    api_instance = mtmaisdk.clients.rest.GithubApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    event = 'event_example' # str | The event key

    try:
        # Github app tenant webhook
        await api_instance.sns_update(tenant, event)
    except Exception as e:
        print("Exception when calling GithubApi->sns_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **event** | **str**| The event key | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully processed webhook |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

