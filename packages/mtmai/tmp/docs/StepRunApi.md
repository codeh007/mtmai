# mtmaisdk.clients.rest.StepRunApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**step_run_get**](StepRunApi.md#step_run_get) | **GET** /api/v1/tenants/{tenant}/step-runs/{step-run} | Get step run
[**step_run_get_schema**](StepRunApi.md#step_run_get_schema) | **GET** /api/v1/tenants/{tenant}/step-runs/{step-run}/schema | Get step run schema
[**step_run_list_archives**](StepRunApi.md#step_run_list_archives) | **GET** /api/v1/step-runs/{step-run}/archives | List archives for step run
[**step_run_list_events**](StepRunApi.md#step_run_list_events) | **GET** /api/v1/step-runs/{step-run}/events | List events for step run
[**step_run_update_cancel**](StepRunApi.md#step_run_update_cancel) | **POST** /api/v1/tenants/{tenant}/step-runs/{step-run}/cancel | Attempts to cancel a step run
[**step_run_update_rerun**](StepRunApi.md#step_run_update_rerun) | **POST** /api/v1/tenants/{tenant}/step-runs/{step-run}/rerun | Rerun step run
[**workflow_run_list_step_run_events**](StepRunApi.md#workflow_run_list_step_run_events) | **GET** /api/v1/tenants/{tenant}/workflow-runs/{workflow-run}/step-run-events | List events for all step runs for a workflow run


# **step_run_get**
> StepRun step_run_get(tenant, step_run)

Get step run

Get a step run by id

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.step_run import StepRun
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    step_run = 'step_run_example' # str | The step run id

    try:
        # Get step run
        api_response = await api_instance.step_run_get(tenant, step_run)
        print("The response of StepRunApi->step_run_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->step_run_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **step_run** | **str**| The step run id | 

### Return type

[**StepRun**](StepRun.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the step run |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | The step run was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **step_run_get_schema**
> object step_run_get_schema(tenant, step_run)

Get step run schema

Get the schema for a step run

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    step_run = 'step_run_example' # str | The step run id

    try:
        # Get step run schema
        api_response = await api_instance.step_run_get_schema(tenant, step_run)
        print("The response of StepRunApi->step_run_get_schema:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->step_run_get_schema: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **step_run** | **str**| The step run id | 

### Return type

**object**

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the step run schema |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | The step run was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **step_run_list_archives**
> StepRunArchiveList step_run_list_archives(step_run, offset=offset, limit=limit)

List archives for step run

List archives for a step run

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.step_run_archive_list import StepRunArchiveList
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    step_run = 'step_run_example' # str | The step run id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)

    try:
        # List archives for step run
        api_response = await api_instance.step_run_list_archives(step_run, offset=offset, limit=limit)
        print("The response of StepRunApi->step_run_list_archives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->step_run_list_archives: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **step_run** | **str**| The step run id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 

### Return type

[**StepRunArchiveList**](StepRunArchiveList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | The step run was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **step_run_list_events**
> StepRunEventList step_run_list_events(step_run, offset=offset, limit=limit)

List events for step run

List events for a step run

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.step_run_event_list import StepRunEventList
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    step_run = 'step_run_example' # str | The step run id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)

    try:
        # List events for step run
        api_response = await api_instance.step_run_list_events(step_run, offset=offset, limit=limit)
        print("The response of StepRunApi->step_run_list_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->step_run_list_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **step_run** | **str**| The step run id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 

### Return type

[**StepRunEventList**](StepRunEventList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | The step run was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **step_run_update_cancel**
> StepRun step_run_update_cancel(tenant, step_run)

Attempts to cancel a step run

Attempts to cancel a step run

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.step_run import StepRun
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    step_run = 'step_run_example' # str | The step run id

    try:
        # Attempts to cancel a step run
        api_response = await api_instance.step_run_update_cancel(tenant, step_run)
        print("The response of StepRunApi->step_run_update_cancel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->step_run_update_cancel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **step_run** | **str**| The step run id | 

### Return type

[**StepRun**](StepRun.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully dispatched the cancellation |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **step_run_update_rerun**
> StepRun step_run_update_rerun(tenant, step_run, rerun_step_run_request)

Rerun step run

Reruns a step run

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.rerun_step_run_request import RerunStepRunRequest
from mtmaisdk.clients.rest.models.step_run import StepRun
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    step_run = 'step_run_example' # str | The step run id
    rerun_step_run_request = mtmaisdk.clients.rest.RerunStepRunRequest() # RerunStepRunRequest | The input to the rerun

    try:
        # Rerun step run
        api_response = await api_instance.step_run_update_rerun(tenant, step_run, rerun_step_run_request)
        print("The response of StepRunApi->step_run_update_rerun:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->step_run_update_rerun: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **step_run** | **str**| The step run id | 
 **rerun_step_run_request** | [**RerunStepRunRequest**](RerunStepRunRequest.md)| The input to the rerun | 

### Return type

[**StepRun**](StepRun.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully replayed the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_list_step_run_events**
> StepRunEventList workflow_run_list_step_run_events(tenant, workflow_run, last_id=last_id)

List events for all step runs for a workflow run

List events for all step runs for a workflow run

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.step_run_event_list import StepRunEventList
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
    api_instance = mtmaisdk.clients.rest.StepRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflow_run = 'workflow_run_example' # str | The workflow run id
    last_id = 56 # int | Last ID of the last event (optional)

    try:
        # List events for all step runs for a workflow run
        api_response = await api_instance.workflow_run_list_step_run_events(tenant, workflow_run, last_id=last_id)
        print("The response of StepRunApi->workflow_run_list_step_run_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StepRunApi->workflow_run_list_step_run_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflow_run** | **str**| The workflow run id | 
 **last_id** | **int**| Last ID of the last event | [optional] 

### Return type

[**StepRunEventList**](StepRunEventList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | The step run was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

