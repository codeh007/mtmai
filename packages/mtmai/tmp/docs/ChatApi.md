# mtmaisdk.clients.rest.ChatApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**chat_create_chat_session**](ChatApi.md#chat_create_chat_session) | **POST** /api/v1/tenants/{tenant}/chats | 创建聊天 Session
[**chat_get**](ChatApi.md#chat_get) | **GET** /api/v1/tenants/{tenant}/chats/{chat} | 获取租户下的聊天列表
[**chat_list**](ChatApi.md#chat_list) | **GET** /api/v1/tenants/{tenant}/chats | 获取租户下的聊天列表
[**chat_messages**](ChatApi.md#chat_messages) | **GET** /api/v1/tenants/{tenant}/chats/{chatId}/messages | 获取聊天消息
[**chat_update_chat_session**](ChatApi.md#chat_update_chat_session) | **PUT** /api/v1/tenants/{tenant}/chats/{chat} | 更新会话


# **chat_create_chat_session**
> ChatSession chat_create_chat_session(tenant, chat_session_update)

创建聊天 Session

创建聊天 Session

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.chat_session import ChatSession
from mtmaisdk.clients.rest.models.chat_session_update import ChatSessionUpdate
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
    api_instance = mtmaisdk.clients.rest.ChatApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    chat_session_update = mtmaisdk.clients.rest.ChatSessionUpdate() # ChatSessionUpdate | 

    try:
        # 创建聊天 Session
        api_response = await api_instance.chat_create_chat_session(tenant, chat_session_update)
        print("The response of ChatApi->chat_create_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->chat_create_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **chat_session_update** | [**ChatSessionUpdate**](ChatSessionUpdate.md)|  | 

### Return type

[**ChatSession**](ChatSession.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **chat_get**
> ChatSession chat_get(tenant, chat)

获取租户下的聊天列表

获取聊天列表

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.chat_session import ChatSession
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
    api_instance = mtmaisdk.clients.rest.ChatApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    chat = 'chat_example' # str | The chat id

    try:
        # 获取租户下的聊天列表
        api_response = await api_instance.chat_get(tenant, chat)
        print("The response of ChatApi->chat_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->chat_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **chat** | **str**| The chat id | 

### Return type

[**ChatSession**](ChatSession.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **chat_list**
> ChatSessionList chat_list(tenant)

获取租户下的聊天列表

获取聊天列表

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.chat_session_list import ChatSessionList
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
    api_instance = mtmaisdk.clients.rest.ChatApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # 获取租户下的聊天列表
        api_response = await api_instance.chat_list(tenant)
        print("The response of ChatApi->chat_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->chat_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

[**ChatSessionList**](ChatSessionList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **chat_messages**
> ChatMessages chat_messages(tenant, chat_id)

获取聊天消息

获取聊天消息

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.chat_messages import ChatMessages
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
    api_instance = mtmaisdk.clients.rest.ChatApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    chat_id = 'chat_id_example' # str | 聊天 ID

    try:
        # 获取聊天消息
        api_response = await api_instance.chat_messages(tenant, chat_id)
        print("The response of ChatApi->chat_messages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->chat_messages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **chat_id** | **str**| 聊天 ID | 

### Return type

[**ChatMessages**](ChatMessages.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 返回聊天消息 |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **chat_update_chat_session**
> ChatSession chat_update_chat_session(tenant, chat, chat_session_update)

更新会话

更新会话

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmaisdk.clients.rest
from mtmaisdk.clients.rest.models.chat_session import ChatSession
from mtmaisdk.clients.rest.models.chat_session_update import ChatSessionUpdate
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
    api_instance = mtmaisdk.clients.rest.ChatApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    chat = 'chat_example' # str | The session id
    chat_session_update = mtmaisdk.clients.rest.ChatSessionUpdate() # ChatSessionUpdate | 

    try:
        # 更新会话
        api_response = await api_instance.chat_update_chat_session(tenant, chat, chat_session_update)
        print("The response of ChatApi->chat_update_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->chat_update_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **chat** | **str**| The session id | 
 **chat_session_update** | [**ChatSessionUpdate**](ChatSessionUpdate.md)|  | 

### Return type

[**ChatSession**](ChatSession.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

