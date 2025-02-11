# mtmaisdk.clients.rest.WorkflowRunApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**workflow_run_cancel**](WorkflowRunApi.md#workflow_run_cancel) | **POST** /api/v1/tenants/{tenant}/workflows/cancel | Cancel workflow runs
[**workflow_run_create**](WorkflowRunApi.md#workflow_run_create) | **POST** /api/v1/workflows/{workflow}/trigger | Trigger workflow run
[**workflow_run_get_input**](WorkflowRunApi.md#workflow_run_get_input) | **GET** /api/v1/tenants/{tenant}/workflow-runs/{workflow-run}/input | Get workflow run input
[**workflow_run_update_replay**](WorkflowRunApi.md#workflow_run_update_replay) | **POST** /api/v1/tenants/{tenant}/workflow-runs/replay | Replay workflow runs


# **workflow_run_cancel**
> EventUpdateCancel200Response workflow_run_cancel(tenant, workflow_runs_cancel_request)

Cancel workflow runs

Cancel a batch of workflow runs

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.event_update_cancel200_response import EventUpdateCancel200Response
from mtmaisdk.clients.rest.models.workflow_runs_cancel_request import WorkflowRunsCancelRequest
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
    api_instance = mtmaisdk.clients.rest.WorkflowRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflow_runs_cancel_request = mtmaisdk.clients.rest.WorkflowRunsCancelRequest() # WorkflowRunsCancelRequest | The input to cancel the workflow runs

    try:
        # Cancel workflow runs
        api_response = await api_instance.workflow_run_cancel(tenant, workflow_runs_cancel_request)
        print("The response of WorkflowRunApi->workflow_run_cancel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowRunApi->workflow_run_cancel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflow_runs_cancel_request** | [**WorkflowRunsCancelRequest**](WorkflowRunsCancelRequest.md)| The input to cancel the workflow runs | 

### Return type

[**EventUpdateCancel200Response**](EventUpdateCancel200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully cancelled the workflow runs |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_create**
> WorkflowRun workflow_run_create(workflow, trigger_workflow_run_request, version=version)

Trigger workflow run

Trigger a new workflow run for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.trigger_workflow_run_request import TriggerWorkflowRunRequest
from mtmaisdk.clients.rest.models.workflow_run import WorkflowRun
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
    api_instance = mtmaisdk.clients.rest.WorkflowRunApi(api_client)
    workflow = 'workflow_example' # str | The workflow id
    trigger_workflow_run_request = mtmaisdk.clients.rest.TriggerWorkflowRunRequest() # TriggerWorkflowRunRequest | The input to the workflow run
    version = 'version_example' # str | The workflow version. If not supplied, the latest version is fetched. (optional)

    try:
        # Trigger workflow run
        api_response = await api_instance.workflow_run_create(workflow, trigger_workflow_run_request, version=version)
        print("The response of WorkflowRunApi->workflow_run_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowRunApi->workflow_run_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow** | **str**| The workflow id | 
 **trigger_workflow_run_request** | [**TriggerWorkflowRunRequest**](TriggerWorkflowRunRequest.md)| The input to the workflow run | 
 **version** | **str**| The workflow version. If not supplied, the latest version is fetched. | [optional] 

### Return type

[**WorkflowRun**](WorkflowRun.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the workflow run |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |
**429** | Resource limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_get_input**
> Dict[str, object] workflow_run_get_input(tenant, workflow_run)

Get workflow run input

Get the input for a workflow run.

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
    api_instance = mtmaisdk.clients.rest.WorkflowRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflow_run = 'workflow_run_example' # str | The workflow run id

    try:
        # Get workflow run input
        api_response = await api_instance.workflow_run_get_input(tenant, workflow_run)
        print("The response of WorkflowRunApi->workflow_run_get_input:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowRunApi->workflow_run_get_input: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflow_run** | **str**| The workflow run id | 

### Return type

**Dict[str, object]**

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow run input |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Workflow run not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_update_replay**
> ReplayWorkflowRunsResponse workflow_run_update_replay(tenant, replay_workflow_runs_request)

Replay workflow runs

Replays a list of workflow runs.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.replay_workflow_runs_request import ReplayWorkflowRunsRequest
from mtmaisdk.clients.rest.models.replay_workflow_runs_response import ReplayWorkflowRunsResponse
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
    api_instance = mtmaisdk.clients.rest.WorkflowRunApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    replay_workflow_runs_request = mtmaisdk.clients.rest.ReplayWorkflowRunsRequest() # ReplayWorkflowRunsRequest | The workflow run ids to replay

    try:
        # Replay workflow runs
        api_response = await api_instance.workflow_run_update_replay(tenant, replay_workflow_runs_request)
        print("The response of WorkflowRunApi->workflow_run_update_replay:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowRunApi->workflow_run_update_replay: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **replay_workflow_runs_request** | [**ReplayWorkflowRunsRequest**](ReplayWorkflowRunsRequest.md)| The workflow run ids to replay | 

### Return type

[**ReplayWorkflowRunsResponse**](ReplayWorkflowRunsResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully replayed the workflow runs |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**429** | Resource limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

