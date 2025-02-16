# mtmai.clients.rest.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tenant_invite_delete**](DefaultApi.md#tenant_invite_delete) | **DELETE** /api/v1/tenants/{tenant}/invites/{tenant-invite} | Delete invite
[**tenant_invite_update**](DefaultApi.md#tenant_invite_update) | **PATCH** /api/v1/tenants/{tenant}/invites/{tenant-invite} | Update invite
[**webhook_create**](DefaultApi.md#webhook_create) | **POST** /api/v1/tenants/{tenant}/webhook-workers | Create a webhook
[**webhook_delete**](DefaultApi.md#webhook_delete) | **DELETE** /api/v1/webhook-workers/{webhook} | Delete a webhook
[**webhook_list**](DefaultApi.md#webhook_list) | **GET** /api/v1/tenants/{tenant}/webhook-workers | List webhooks
[**webhook_requests_list**](DefaultApi.md#webhook_requests_list) | **GET** /api/v1/webhook-workers/{webhook}/requests | List webhook requests
[**worker_config**](DefaultApi.md#worker_config) | **GET** /api/v1/worker/config | 获取worker配置, 内部使用免去配置 token环境变量的麻烦


# **tenant_invite_delete**
> TenantInvite tenant_invite_delete(tenant, tenant_invite)

Delete invite

Deletes a tenant invite

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.tenant_invite import TenantInvite
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    tenant_invite = 'tenant_invite_example' # str | The tenant invite id

    try:
        # Delete invite
        api_response = await api_instance.tenant_invite_delete(tenant, tenant_invite)
        print("The response of DefaultApi->tenant_invite_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->tenant_invite_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **tenant_invite** | **str**| The tenant invite id | 

### Return type

[**TenantInvite**](TenantInvite.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully deleted the tenant invite |  -  |
**400** | A malformed or bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tenant_invite_update**
> TenantInvite tenant_invite_update(tenant, tenant_invite, update_tenant_invite_request)

Update invite

Updates a tenant invite

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.tenant_invite import TenantInvite
from mtmai.clients.rest.models.update_tenant_invite_request import UpdateTenantInviteRequest
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    tenant_invite = 'tenant_invite_example' # str | The tenant invite id
    update_tenant_invite_request = mtmai.clients.rest.UpdateTenantInviteRequest() # UpdateTenantInviteRequest | The tenant invite to update

    try:
        # Update invite
        api_response = await api_instance.tenant_invite_update(tenant, tenant_invite, update_tenant_invite_request)
        print("The response of DefaultApi->tenant_invite_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->tenant_invite_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **tenant_invite** | **str**| The tenant invite id | 
 **update_tenant_invite_request** | [**UpdateTenantInviteRequest**](UpdateTenantInviteRequest.md)| The tenant invite to update | 

### Return type

[**TenantInvite**](TenantInvite.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated the tenant invite |  -  |
**400** | A malformed or bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **webhook_create**
> WebhookWorkerCreated webhook_create(tenant, webhook_worker_create_request=webhook_worker_create_request)

Create a webhook

Creates a webhook

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.webhook_worker_create_request import WebhookWorkerCreateRequest
from mtmai.clients.rest.models.webhook_worker_created import WebhookWorkerCreated
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    webhook_worker_create_request = mtmai.clients.rest.WebhookWorkerCreateRequest() # WebhookWorkerCreateRequest |  (optional)

    try:
        # Create a webhook
        api_response = await api_instance.webhook_create(tenant, webhook_worker_create_request=webhook_worker_create_request)
        print("The response of DefaultApi->webhook_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->webhook_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **webhook_worker_create_request** | [**WebhookWorkerCreateRequest**](WebhookWorkerCreateRequest.md)|  | [optional] 

### Return type

[**WebhookWorkerCreated**](WebhookWorkerCreated.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the webhook |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **webhook_delete**
> webhook_delete(webhook)

Delete a webhook

Deletes a webhook

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)
    webhook = 'webhook_example' # str | The webhook id

    try:
        # Delete a webhook
        await api_instance.webhook_delete(webhook)
    except Exception as e:
        print("Exception when calling DefaultApi->webhook_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webhook** | **str**| The webhook id | 

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
**200** | Successfully deleted the webhook |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **webhook_list**
> WebhookWorkerListResponse webhook_list(tenant)

List webhooks

Lists all webhooks

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.webhook_worker_list_response import WebhookWorkerListResponse
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # List webhooks
        api_response = await api_instance.webhook_list(tenant)
        print("The response of DefaultApi->webhook_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->webhook_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

[**WebhookWorkerListResponse**](WebhookWorkerListResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of webhook workers |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **webhook_requests_list**
> WebhookWorkerRequestListResponse webhook_requests_list(webhook)

List webhook requests

Lists all requests for a webhook

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.webhook_worker_request_list_response import WebhookWorkerRequestListResponse
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)
    webhook = 'webhook_example' # str | The webhook id

    try:
        # List webhook requests
        api_response = await api_instance.webhook_requests_list(webhook)
        print("The response of DefaultApi->webhook_requests_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->webhook_requests_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webhook** | **str**| The webhook id | 

### Return type

[**WebhookWorkerRequestListResponse**](WebhookWorkerRequestListResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of webhook requests |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **worker_config**
> WorkerConfig worker_config()

获取worker配置, 内部使用免去配置 token环境变量的麻烦

获取worker配置

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.worker_config import WorkerConfig
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
    api_instance = mtmai.clients.rest.DefaultApi(api_client)

    try:
        # 获取worker配置, 内部使用免去配置 token环境变量的麻烦
        api_response = await api_instance.worker_config()
        print("The response of DefaultApi->worker_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->worker_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**WorkerConfig**](WorkerConfig.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 返回模型列表 |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

