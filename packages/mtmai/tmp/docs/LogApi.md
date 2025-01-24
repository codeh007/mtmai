# mtmai.gomtmclients.rest.LogApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**log_line_list**](LogApi.md#log_line_list) | **GET** /api/v1/step-runs/{step-run}/logs | List log lines


# **log_line_list**
> LogLineList log_line_list(step_run, offset=offset, limit=limit, levels=levels, search=search, order_by_field=order_by_field, order_by_direction=order_by_direction)

List log lines

Lists log lines for a step run.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.log_line_level import LogLineLevel
from mtmai.gomtmclients.rest.models.log_line_list import LogLineList
from mtmai.gomtmclients.rest.models.log_line_order_by_direction import LogLineOrderByDirection
from mtmai.gomtmclients.rest.models.log_line_order_by_field import LogLineOrderByField
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
    api_instance = mtmai.gomtmclients.rest.LogApi(api_client)
    step_run = 'step_run_example' # str | The step run id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)
    levels = [mtmai.gomtmclients.rest.LogLineLevel()] # List[LogLineLevel] | A list of levels to filter by (optional)
    search = 'search_example' # str | The search query to filter for (optional)
    order_by_field = mtmai.gomtmclients.rest.LogLineOrderByField() # LogLineOrderByField | What to order by (optional)
    order_by_direction = mtmai.gomtmclients.rest.LogLineOrderByDirection() # LogLineOrderByDirection | The order direction (optional)

    try:
        # List log lines
        api_response = await api_instance.log_line_list(step_run, offset=offset, limit=limit, levels=levels, search=search, order_by_field=order_by_field, order_by_direction=order_by_direction)
        print("The response of LogApi->log_line_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LogApi->log_line_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **step_run** | **str**| The step run id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 
 **levels** | [**List[LogLineLevel]**](LogLineLevel.md)| A list of levels to filter by | [optional] 
 **search** | **str**| The search query to filter for | [optional] 
 **order_by_field** | [**LogLineOrderByField**](.md)| What to order by | [optional] 
 **order_by_direction** | [**LogLineOrderByDirection**](.md)| The order direction | [optional] 

### Return type

[**LogLineList**](LogLineList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

