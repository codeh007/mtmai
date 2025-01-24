# mtmai.gomtmclients.rest.WorkflowApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cron_workflow_list**](WorkflowApi.md#cron_workflow_list) | **GET** /api/v1/tenants/{tenant}/workflows/crons | Get cron job workflows
[**tenant_get_queue_metrics**](WorkflowApi.md#tenant_get_queue_metrics) | **GET** /api/v1/tenants/{tenant}/queue-metrics | Get workflow metrics
[**workflow_delete**](WorkflowApi.md#workflow_delete) | **DELETE** /api/v1/workflows/{workflow} | Delete workflow
[**workflow_get**](WorkflowApi.md#workflow_get) | **GET** /api/v1/workflows/{workflow} | Get workflow
[**workflow_get_by_name**](WorkflowApi.md#workflow_get_by_name) | **GET** /api/v1/tenants/{tenant}/workflows/byName/{name} | Get workflow version
[**workflow_get_metrics**](WorkflowApi.md#workflow_get_metrics) | **GET** /api/v1/workflows/{workflow}/metrics | Get workflow metrics
[**workflow_get_workers_count**](WorkflowApi.md#workflow_get_workers_count) | **GET** /api/v1/tenants/{tenant}/workflows/{workflow}/worker-count | Get workflow worker count
[**workflow_list**](WorkflowApi.md#workflow_list) | **GET** /api/v1/tenants/{tenant}/workflows | Get workflows
[**workflow_run_get**](WorkflowApi.md#workflow_run_get) | **GET** /api/v1/tenants/{tenant}/workflow-runs/{workflow-run} | Get workflow run
[**workflow_run_get_metrics**](WorkflowApi.md#workflow_run_get_metrics) | **GET** /api/v1/tenants/{tenant}/workflows/runs/metrics | Get workflow runs metrics
[**workflow_run_get_shape**](WorkflowApi.md#workflow_run_get_shape) | **GET** /api/v1/tenants/{tenant}/workflow-runs/{workflow-run}/shape | Get workflow run
[**workflow_run_list**](WorkflowApi.md#workflow_run_list) | **GET** /api/v1/tenants/{tenant}/workflows/runs | Get workflow runs
[**workflow_scheduled_delete**](WorkflowApi.md#workflow_scheduled_delete) | **DELETE** /api/v1/tenants/{tenant}/workflows/scheduled/{scheduledId} | Delete scheduled workflow run
[**workflow_scheduled_get**](WorkflowApi.md#workflow_scheduled_get) | **GET** /api/v1/tenants/{tenant}/workflows/scheduled/{scheduledId} | Get scheduled workflow run
[**workflow_scheduled_list**](WorkflowApi.md#workflow_scheduled_list) | **GET** /api/v1/tenants/{tenant}/workflows/scheduled | Get scheduled workflow runs
[**workflow_update**](WorkflowApi.md#workflow_update) | **PATCH** /api/v1/workflows/{workflow} | Update workflow
[**workflow_version_get**](WorkflowApi.md#workflow_version_get) | **GET** /api/v1/workflows/{workflow}/versions | Get workflow version


# **cron_workflow_list**
> CronWorkflowsList cron_workflow_list(tenant, offset=offset, limit=limit, workflow_id=workflow_id, additional_metadata=additional_metadata, order_by_field=order_by_field, order_by_direction=order_by_direction)

Get cron job workflows

Get all cron job workflow runs for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.cron_workflows_list import CronWorkflowsList
from mtmai.gomtmclients.rest.models.cron_workflows_order_by_field import CronWorkflowsOrderByField
from mtmai.gomtmclients.rest.models.workflow_run_order_by_direction import WorkflowRunOrderByDirection
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)
    workflow_id = 'workflow_id_example' # str | The workflow id to get runs for. (optional)
    additional_metadata = ['[key1:value1, key2:value2]'] # List[str] | A list of metadata key value pairs to filter by (optional)
    order_by_field = mtmai.gomtmclients.rest.CronWorkflowsOrderByField() # CronWorkflowsOrderByField | The order by field (optional)
    order_by_direction = mtmai.gomtmclients.rest.WorkflowRunOrderByDirection() # WorkflowRunOrderByDirection | The order by direction (optional)

    try:
        # Get cron job workflows
        api_response = await api_instance.cron_workflow_list(tenant, offset=offset, limit=limit, workflow_id=workflow_id, additional_metadata=additional_metadata, order_by_field=order_by_field, order_by_direction=order_by_direction)
        print("The response of WorkflowApi->cron_workflow_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->cron_workflow_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 
 **workflow_id** | **str**| The workflow id to get runs for. | [optional] 
 **additional_metadata** | [**List[str]**](str.md)| A list of metadata key value pairs to filter by | [optional] 
 **order_by_field** | [**CronWorkflowsOrderByField**](.md)| The order by field | [optional] 
 **order_by_direction** | [**WorkflowRunOrderByDirection**](.md)| The order by direction | [optional] 

### Return type

[**CronWorkflowsList**](CronWorkflowsList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow runs |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tenant_get_queue_metrics**
> TenantQueueMetrics tenant_get_queue_metrics(tenant, workflows=workflows, additional_metadata=additional_metadata)

Get workflow metrics

Get the queue metrics for the tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.tenant_queue_metrics import TenantQueueMetrics
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflows = ['workflows_example'] # List[str] | A list of workflow IDs to filter by (optional)
    additional_metadata = ['[\"key1:value1\",\"key2:value2\"]'] # List[str] | A list of metadata key value pairs to filter by (optional)

    try:
        # Get workflow metrics
        api_response = await api_instance.tenant_get_queue_metrics(tenant, workflows=workflows, additional_metadata=additional_metadata)
        print("The response of WorkflowApi->tenant_get_queue_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->tenant_get_queue_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflows** | [**List[str]**](str.md)| A list of workflow IDs to filter by | [optional] 
 **additional_metadata** | [**List[str]**](str.md)| A list of metadata key value pairs to filter by | [optional] 

### Return type

[**TenantQueueMetrics**](TenantQueueMetrics.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow version metrics |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_delete**
> workflow_delete(workflow)

Delete workflow

Delete a workflow for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    workflow = 'workflow_example' # str | The workflow id

    try:
        # Delete workflow
        await api_instance.workflow_delete(workflow)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow** | **str**| The workflow id | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted the workflow |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_get**
> Workflow workflow_get(workflow)

Get workflow

Get a workflow for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow import Workflow
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    workflow = 'workflow_example' # str | The workflow id

    try:
        # Get workflow
        api_response = await api_instance.workflow_get(workflow)
        print("The response of WorkflowApi->workflow_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow** | **str**| The workflow id | 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_get_by_name**
> Workflow workflow_get_by_name(tenant, name)

Get workflow version

Get a workflow by its name

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow import Workflow
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    name = 'name_example' # str | The workflow name

    try:
        # Get workflow version
        api_response = await api_instance.workflow_get_by_name(tenant, name)
        print("The response of WorkflowApi->workflow_get_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_get_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **name** | **str**| The workflow name | 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_get_metrics**
> WorkflowMetrics workflow_get_metrics(workflow, status=status, group_key=group_key)

Get workflow metrics

Get the metrics for a workflow version

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_metrics import WorkflowMetrics
from mtmai.gomtmclients.rest.models.workflow_run_status import WorkflowRunStatus
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    workflow = 'workflow_example' # str | The workflow id
    status = mtmai.gomtmclients.rest.WorkflowRunStatus() # WorkflowRunStatus | A status of workflow run statuses to filter by (optional)
    group_key = 'group_key_example' # str | A group key to filter metrics by (optional)

    try:
        # Get workflow metrics
        api_response = await api_instance.workflow_get_metrics(workflow, status=status, group_key=group_key)
        print("The response of WorkflowApi->workflow_get_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_get_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow** | **str**| The workflow id | 
 **status** | [**WorkflowRunStatus**](.md)| A status of workflow run statuses to filter by | [optional] 
 **group_key** | **str**| A group key to filter metrics by | [optional] 

### Return type

[**WorkflowMetrics**](WorkflowMetrics.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow version metrics |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_get_workers_count**
> WorkflowWorkersCount workflow_get_workers_count(tenant, workflow)

Get workflow worker count

Get a count of the workers available for workflow

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_workers_count import WorkflowWorkersCount
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflow = 'workflow_example' # str | The workflow id

    try:
        # Get workflow worker count
        api_response = await api_instance.workflow_get_workers_count(tenant, workflow)
        print("The response of WorkflowApi->workflow_get_workers_count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_get_workers_count: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflow** | **str**| The workflow id | 

### Return type

[**WorkflowWorkersCount**](WorkflowWorkersCount.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow worker count |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_list**
> WorkflowList workflow_list(tenant)

Get workflows

Get all workflows for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_list import WorkflowList
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # Get workflows
        api_response = await api_instance.workflow_list(tenant)
        print("The response of WorkflowApi->workflow_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

[**WorkflowList**](WorkflowList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflows |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_get**
> WorkflowRun workflow_run_get(tenant, workflow_run)

Get workflow run

Get a workflow run for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_run import WorkflowRun
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflow_run = 'workflow_run_example' # str | The workflow run id

    try:
        # Get workflow run
        api_response = await api_instance.workflow_run_get(tenant, workflow_run)
        print("The response of WorkflowApi->workflow_run_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_run_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflow_run** | **str**| The workflow run id | 

### Return type

[**WorkflowRun**](WorkflowRun.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow run |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_get_metrics**
> WorkflowRunsMetrics workflow_run_get_metrics(tenant, event_id=event_id, workflow_id=workflow_id, parent_workflow_run_id=parent_workflow_run_id, parent_step_run_id=parent_step_run_id, additional_metadata=additional_metadata, created_after=created_after, created_before=created_before)

Get workflow runs metrics

Get a summary of  workflow run metrics for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_runs_metrics import WorkflowRunsMetrics
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    event_id = 'event_id_example' # str | The event id to get runs for. (optional)
    workflow_id = 'workflow_id_example' # str | The workflow id to get runs for. (optional)
    parent_workflow_run_id = 'parent_workflow_run_id_example' # str | The parent workflow run id (optional)
    parent_step_run_id = 'parent_step_run_id_example' # str | The parent step run id (optional)
    additional_metadata = ['[key1:value1, key2:value2]'] # List[str] | A list of metadata key value pairs to filter by (optional)
    created_after = '2021-01-01T00:00:00Z' # datetime | The time after the workflow run was created (optional)
    created_before = '2021-01-01T00:00:00Z' # datetime | The time before the workflow run was created (optional)

    try:
        # Get workflow runs metrics
        api_response = await api_instance.workflow_run_get_metrics(tenant, event_id=event_id, workflow_id=workflow_id, parent_workflow_run_id=parent_workflow_run_id, parent_step_run_id=parent_step_run_id, additional_metadata=additional_metadata, created_after=created_after, created_before=created_before)
        print("The response of WorkflowApi->workflow_run_get_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_run_get_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **event_id** | **str**| The event id to get runs for. | [optional] 
 **workflow_id** | **str**| The workflow id to get runs for. | [optional] 
 **parent_workflow_run_id** | **str**| The parent workflow run id | [optional] 
 **parent_step_run_id** | **str**| The parent step run id | [optional] 
 **additional_metadata** | [**List[str]**](str.md)| A list of metadata key value pairs to filter by | [optional] 
 **created_after** | **datetime**| The time after the workflow run was created | [optional] 
 **created_before** | **datetime**| The time before the workflow run was created | [optional] 

### Return type

[**WorkflowRunsMetrics**](WorkflowRunsMetrics.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow runs metrics |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_get_shape**
> WorkflowRunShape workflow_run_get_shape(tenant, workflow_run)

Get workflow run

Get a workflow run for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_run_shape import WorkflowRunShape
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    workflow_run = 'workflow_run_example' # str | The workflow run id

    try:
        # Get workflow run
        api_response = await api_instance.workflow_run_get_shape(tenant, workflow_run)
        print("The response of WorkflowApi->workflow_run_get_shape:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_run_get_shape: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **workflow_run** | **str**| The workflow run id | 

### Return type

[**WorkflowRunShape**](WorkflowRunShape.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow run |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_run_list**
> WorkflowRunList workflow_run_list(tenant, offset=offset, limit=limit, event_id=event_id, workflow_id=workflow_id, parent_workflow_run_id=parent_workflow_run_id, parent_step_run_id=parent_step_run_id, statuses=statuses, kinds=kinds, additional_metadata=additional_metadata, created_after=created_after, created_before=created_before, finished_after=finished_after, finished_before=finished_before, order_by_field=order_by_field, order_by_direction=order_by_direction)

Get workflow runs

Get all workflow runs for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_kind import WorkflowKind
from mtmai.gomtmclients.rest.models.workflow_run_list import WorkflowRunList
from mtmai.gomtmclients.rest.models.workflow_run_order_by_direction import WorkflowRunOrderByDirection
from mtmai.gomtmclients.rest.models.workflow_run_order_by_field import WorkflowRunOrderByField
from mtmai.gomtmclients.rest.models.workflow_run_status import WorkflowRunStatus
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)
    event_id = 'event_id_example' # str | The event id to get runs for. (optional)
    workflow_id = 'workflow_id_example' # str | The workflow id to get runs for. (optional)
    parent_workflow_run_id = 'parent_workflow_run_id_example' # str | The parent workflow run id (optional)
    parent_step_run_id = 'parent_step_run_id_example' # str | The parent step run id (optional)
    statuses = [mtmai.gomtmclients.rest.WorkflowRunStatus()] # List[WorkflowRunStatus] | A list of workflow run statuses to filter by (optional)
    kinds = [mtmai.gomtmclients.rest.WorkflowKind()] # List[WorkflowKind] | A list of workflow kinds to filter by (optional)
    additional_metadata = ['[key1:value1, key2:value2]'] # List[str] | A list of metadata key value pairs to filter by (optional)
    created_after = '2021-01-01T00:00:00Z' # datetime | The time after the workflow run was created (optional)
    created_before = '2021-01-01T00:00:00Z' # datetime | The time before the workflow run was created (optional)
    finished_after = '2021-01-01T00:00:00Z' # datetime | The time after the workflow run was finished (optional)
    finished_before = '2021-01-01T00:00:00Z' # datetime | The time before the workflow run was finished (optional)
    order_by_field = mtmai.gomtmclients.rest.WorkflowRunOrderByField() # WorkflowRunOrderByField | The order by field (optional)
    order_by_direction = mtmai.gomtmclients.rest.WorkflowRunOrderByDirection() # WorkflowRunOrderByDirection | The order by direction (optional)

    try:
        # Get workflow runs
        api_response = await api_instance.workflow_run_list(tenant, offset=offset, limit=limit, event_id=event_id, workflow_id=workflow_id, parent_workflow_run_id=parent_workflow_run_id, parent_step_run_id=parent_step_run_id, statuses=statuses, kinds=kinds, additional_metadata=additional_metadata, created_after=created_after, created_before=created_before, finished_after=finished_after, finished_before=finished_before, order_by_field=order_by_field, order_by_direction=order_by_direction)
        print("The response of WorkflowApi->workflow_run_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_run_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 
 **event_id** | **str**| The event id to get runs for. | [optional] 
 **workflow_id** | **str**| The workflow id to get runs for. | [optional] 
 **parent_workflow_run_id** | **str**| The parent workflow run id | [optional] 
 **parent_step_run_id** | **str**| The parent step run id | [optional] 
 **statuses** | [**List[WorkflowRunStatus]**](WorkflowRunStatus.md)| A list of workflow run statuses to filter by | [optional] 
 **kinds** | [**List[WorkflowKind]**](WorkflowKind.md)| A list of workflow kinds to filter by | [optional] 
 **additional_metadata** | [**List[str]**](str.md)| A list of metadata key value pairs to filter by | [optional] 
 **created_after** | **datetime**| The time after the workflow run was created | [optional] 
 **created_before** | **datetime**| The time before the workflow run was created | [optional] 
 **finished_after** | **datetime**| The time after the workflow run was finished | [optional] 
 **finished_before** | **datetime**| The time before the workflow run was finished | [optional] 
 **order_by_field** | [**WorkflowRunOrderByField**](.md)| The order by field | [optional] 
 **order_by_direction** | [**WorkflowRunOrderByDirection**](.md)| The order by direction | [optional] 

### Return type

[**WorkflowRunList**](WorkflowRunList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow runs |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_scheduled_delete**
> workflow_scheduled_delete(tenant, scheduled_id)

Delete scheduled workflow run

Delete a scheduled workflow run for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    scheduled_id = 'scheduled_id_example' # str | The scheduled workflow id

    try:
        # Delete scheduled workflow run
        await api_instance.workflow_scheduled_delete(tenant, scheduled_id)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_scheduled_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **scheduled_id** | **str**| The scheduled workflow id | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted the scheduled workflow run |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_scheduled_get**
> ScheduledWorkflows workflow_scheduled_get(tenant, scheduled_id)

Get scheduled workflow run

Get a scheduled workflow run for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.scheduled_workflows import ScheduledWorkflows
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    scheduled_id = 'scheduled_id_example' # str | The scheduled workflow id

    try:
        # Get scheduled workflow run
        api_response = await api_instance.workflow_scheduled_get(tenant, scheduled_id)
        print("The response of WorkflowApi->workflow_scheduled_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_scheduled_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **scheduled_id** | **str**| The scheduled workflow id | 

### Return type

[**ScheduledWorkflows**](ScheduledWorkflows.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow runs |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_scheduled_list**
> ScheduledWorkflowsList workflow_scheduled_list(tenant, offset=offset, limit=limit, order_by_field=order_by_field, order_by_direction=order_by_direction, workflow_id=workflow_id, parent_workflow_run_id=parent_workflow_run_id, parent_step_run_id=parent_step_run_id, additional_metadata=additional_metadata, statuses=statuses)

Get scheduled workflow runs

Get all scheduled workflow runs for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.scheduled_run_status import ScheduledRunStatus
from mtmai.gomtmclients.rest.models.scheduled_workflows_list import ScheduledWorkflowsList
from mtmai.gomtmclients.rest.models.scheduled_workflows_order_by_field import ScheduledWorkflowsOrderByField
from mtmai.gomtmclients.rest.models.workflow_run_order_by_direction import WorkflowRunOrderByDirection
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)
    order_by_field = mtmai.gomtmclients.rest.ScheduledWorkflowsOrderByField() # ScheduledWorkflowsOrderByField | The order by field (optional)
    order_by_direction = mtmai.gomtmclients.rest.WorkflowRunOrderByDirection() # WorkflowRunOrderByDirection | The order by direction (optional)
    workflow_id = 'workflow_id_example' # str | The workflow id to get runs for. (optional)
    parent_workflow_run_id = 'parent_workflow_run_id_example' # str | The parent workflow run id (optional)
    parent_step_run_id = 'parent_step_run_id_example' # str | The parent step run id (optional)
    additional_metadata = ['[key1:value1, key2:value2]'] # List[str] | A list of metadata key value pairs to filter by (optional)
    statuses = [mtmai.gomtmclients.rest.ScheduledRunStatus()] # List[ScheduledRunStatus] | A list of scheduled run statuses to filter by (optional)

    try:
        # Get scheduled workflow runs
        api_response = await api_instance.workflow_scheduled_list(tenant, offset=offset, limit=limit, order_by_field=order_by_field, order_by_direction=order_by_direction, workflow_id=workflow_id, parent_workflow_run_id=parent_workflow_run_id, parent_step_run_id=parent_step_run_id, additional_metadata=additional_metadata, statuses=statuses)
        print("The response of WorkflowApi->workflow_scheduled_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_scheduled_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 
 **order_by_field** | [**ScheduledWorkflowsOrderByField**](.md)| The order by field | [optional] 
 **order_by_direction** | [**WorkflowRunOrderByDirection**](.md)| The order by direction | [optional] 
 **workflow_id** | **str**| The workflow id to get runs for. | [optional] 
 **parent_workflow_run_id** | **str**| The parent workflow run id | [optional] 
 **parent_step_run_id** | **str**| The parent step run id | [optional] 
 **additional_metadata** | [**List[str]**](str.md)| A list of metadata key value pairs to filter by | [optional] 
 **statuses** | [**List[ScheduledRunStatus]**](ScheduledRunStatus.md)| A list of scheduled run statuses to filter by | [optional] 

### Return type

[**ScheduledWorkflowsList**](ScheduledWorkflowsList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow runs |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_update**
> Workflow workflow_update(workflow, workflow_update_request)

Update workflow

Update a workflow for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow import Workflow
from mtmai.gomtmclients.rest.models.workflow_update_request import WorkflowUpdateRequest
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    workflow = 'workflow_example' # str | The workflow id
    workflow_update_request = mtmai.gomtmclients.rest.WorkflowUpdateRequest() # WorkflowUpdateRequest | The input to update the workflow

    try:
        # Update workflow
        api_response = await api_instance.workflow_update(workflow, workflow_update_request)
        print("The response of WorkflowApi->workflow_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow** | **str**| The workflow id | 
 **workflow_update_request** | [**WorkflowUpdateRequest**](WorkflowUpdateRequest.md)| The input to update the workflow | 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated the workflow |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workflow_version_get**
> WorkflowVersion workflow_version_get(workflow, version=version)

Get workflow version

Get a workflow version for a tenant

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.workflow_version import WorkflowVersion
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
    api_instance = mtmai.gomtmclients.rest.WorkflowApi(api_client)
    workflow = 'workflow_example' # str | The workflow id
    version = 'version_example' # str | The workflow version. If not supplied, the latest version is fetched. (optional)

    try:
        # Get workflow version
        api_response = await api_instance.workflow_version_get(workflow, version=version)
        print("The response of WorkflowApi->workflow_version_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkflowApi->workflow_version_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow** | **str**| The workflow id | 
 **version** | **str**| The workflow version. If not supplied, the latest version is fetched. | [optional] 

### Return type

[**WorkflowVersion**](WorkflowVersion.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the workflow version |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

