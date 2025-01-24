# mtmai.gomtmclients.rest.AgentApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**agent_create**](AgentApi.md#agent_create) | **POST** /api/v1/tenants/{tenant}/nodes | Create agent node
[**agent_node**](AgentApi.md#agent_node) | **GET** /api/v1/tenants/{tenant}/nodes/{node} | 获取节点状态
[**agent_node_form**](AgentApi.md#agent_node_form) | **POST** /api/v1/tenants/{tenant}/nodes/form/{node} | 获取节点表单
[**agent_node_list**](AgentApi.md#agent_node_list) | **GET** /api/v1/tenants/{tenant}/nodes | 获取租户下的节点列表
[**agent_node_run**](AgentApi.md#agent_node_run) | **POST** /api/v1/tenants/{tenant}/nodes/run | 执行节点
[**agent_node_update**](AgentApi.md#agent_node_update) | **PATCH** /api/v1/tenants/{tenant}/nodes/{node} | 更新节点状态


# **agent_create**
> AgentNode agent_create(tenant, agent_node_create_request)

Create agent node

Creates a new agentnode

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.agent_node import AgentNode
from mtmai.gomtmclients.rest.models.agent_node_create_request import AgentNodeCreateRequest
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
    api_instance = mtmai.gomtmclients.rest.AgentApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    agent_node_create_request = mtmai.gomtmclients.rest.AgentNodeCreateRequest() # AgentNodeCreateRequest | 创建agentnode

    try:
        # Create agent node
        api_response = await api_instance.agent_create(tenant, agent_node_create_request)
        print("The response of AgentApi->agent_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentApi->agent_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **agent_node_create_request** | [**AgentNodeCreateRequest**](AgentNodeCreateRequest.md)| 创建agentnode | 

### Return type

[**AgentNode**](AgentNode.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the blog post |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **agent_node**
> AgentNode agent_node(tenant, node)

获取节点状态

获取节点状态

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.agent_node import AgentNode
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
    api_instance = mtmai.gomtmclients.rest.AgentApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    node = 'node_example' # str | The node id

    try:
        # 获取节点状态
        api_response = await api_instance.agent_node(tenant, node)
        print("The response of AgentApi->agent_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentApi->agent_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **node** | **str**| The node id | 

### Return type

[**AgentNode**](AgentNode.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent node full state |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **agent_node_form**
> AgentRunForm agent_node_form(tenant, node)

获取节点表单

获取节点表单

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.agent_run_form import AgentRunForm
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
    api_instance = mtmai.gomtmclients.rest.AgentApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    node = 'node_example' # str | The node id

    try:
        # 获取节点表单
        api_response = await api_instance.agent_node_form(tenant, node)
        print("The response of AgentApi->agent_node_form:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentApi->agent_node_form: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **node** | **str**| The node id | 

### Return type

[**AgentRunForm**](AgentRunForm.md)

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **agent_node_list**
> AgentNodeList agent_node_list(tenant)

获取租户下的节点列表

获取节点

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.agent_node_list import AgentNodeList
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
    api_instance = mtmai.gomtmclients.rest.AgentApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # 获取租户下的节点列表
        api_response = await api_instance.agent_node_list(tenant)
        print("The response of AgentApi->agent_node_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentApi->agent_node_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

[**AgentNodeList**](AgentNodeList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the list of nodes |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **agent_node_run**
> AgentNodeRun agent_node_run(tenant, agent_node_run_input)

执行节点

执行节点(执行工作流)

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.agent_node_run import AgentNodeRun
from mtmai.gomtmclients.rest.models.agent_node_run_input import AgentNodeRunInput
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
    api_instance = mtmai.gomtmclients.rest.AgentApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    agent_node_run_input = mtmai.gomtmclients.rest.AgentNodeRunInput() # AgentNodeRunInput | 创建agentnode

    try:
        # 执行节点
        api_response = await api_instance.agent_node_run(tenant, agent_node_run_input)
        print("The response of AgentApi->agent_node_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentApi->agent_node_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **agent_node_run_input** | [**AgentNodeRunInput**](AgentNodeRunInput.md)| 创建agentnode | 

### Return type

[**AgentNodeRun**](AgentNodeRun.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/event-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **agent_node_update**
> AgentNode agent_node_update(tenant, node, agent_node_update_request)

更新节点状态

更新节点状态

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.gomtmclients.rest
from mtmai.gomtmclients.rest.models.agent_node import AgentNode
from mtmai.gomtmclients.rest.models.agent_node_update_request import AgentNodeUpdateRequest
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
    api_instance = mtmai.gomtmclients.rest.AgentApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    node = 'node_example' # str | The node id
    agent_node_update_request = mtmai.gomtmclients.rest.AgentNodeUpdateRequest() # AgentNodeUpdateRequest | 创建agentnode

    try:
        # 更新节点状态
        api_response = await api_instance.agent_node_update(tenant, node, agent_node_update_request)
        print("The response of AgentApi->agent_node_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentApi->agent_node_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **node** | **str**| The node id | 
 **agent_node_update_request** | [**AgentNodeUpdateRequest**](AgentNodeUpdateRequest.md)| 创建agentnode | 

### Return type

[**AgentNode**](AgentNode.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the blog post |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

