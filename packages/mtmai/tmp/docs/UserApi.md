# mtmai.clients.rest.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tenant_memberships_list**](UserApi.md#tenant_memberships_list) | **GET** /api/v1/users/memberships | List tenant memberships
[**user_create**](UserApi.md#user_create) | **POST** /api/v1/users/register | Register user
[**user_get_current**](UserApi.md#user_get_current) | **GET** /api/v1/users/current | Get current user
[**user_update_github_oauth_callback**](UserApi.md#user_update_github_oauth_callback) | **GET** /api/v1/users/github/callback | Complete OAuth flow
[**user_update_github_oauth_start**](UserApi.md#user_update_github_oauth_start) | **GET** /api/v1/users/github/start | Start OAuth flow
[**user_update_google_oauth_callback**](UserApi.md#user_update_google_oauth_callback) | **GET** /api/v1/users/google/callback | Complete OAuth flow
[**user_update_google_oauth_start**](UserApi.md#user_update_google_oauth_start) | **GET** /api/v1/users/google/start | Start OAuth flow
[**user_update_login**](UserApi.md#user_update_login) | **POST** /api/v1/users/login | Login user
[**user_update_logout**](UserApi.md#user_update_logout) | **POST** /api/v1/users/logout | Logout user
[**user_update_password**](UserApi.md#user_update_password) | **POST** /api/v1/users/password | Change user password
[**user_update_slack_oauth_callback**](UserApi.md#user_update_slack_oauth_callback) | **GET** /api/v1/users/slack/callback | Complete OAuth flow
[**user_update_slack_oauth_start**](UserApi.md#user_update_slack_oauth_start) | **GET** /api/v1/tenants/{tenant}/slack/start | Start OAuth flow


# **tenant_memberships_list**
> UserTenantMembershipsList tenant_memberships_list()

List tenant memberships

Lists all tenant memberships for the current user

### Example

* Api Key Authentication (cookieAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.user_tenant_memberships_list import UserTenantMembershipsList
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

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # List tenant memberships
        api_response = await api_instance.tenant_memberships_list()
        print("The response of UserApi->tenant_memberships_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->tenant_memberships_list: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserTenantMembershipsList**](UserTenantMembershipsList.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed the tenant memberships |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_create**
> User user_create(user_register_request=user_register_request)

Register user

Registers a user.

### Example


```python
import mtmai.clients.rest
from mtmai.clients.rest.models.user import User
from mtmai.clients.rest.models.user_register_request import UserRegisterRequest
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
    api_instance = mtmai.clients.rest.UserApi(api_client)
    user_register_request = mtmai.clients.rest.UserRegisterRequest() # UserRegisterRequest |  (optional)

    try:
        # Register user
        api_response = await api_instance.user_create(user_register_request=user_register_request)
        print("The response of UserApi->user_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->user_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_register_request** | [**UserRegisterRequest**](UserRegisterRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully registered the user |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_get_current**
> User user_get_current()

Get current user

Gets the current user

### Example

* Api Key Authentication (cookieAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.user import User
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

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Get current user
        api_response = await api_instance.user_get_current()
        print("The response of UserApi->user_get_current:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->user_get_current: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the user |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_github_oauth_callback**
> user_update_github_oauth_callback()

Complete OAuth flow

Completes the OAuth flow

### Example


```python
import mtmai.clients.rest
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
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Complete OAuth flow
        await api_instance.user_update_github_oauth_callback()
    except Exception as e:
        print("Exception when calling UserApi->user_update_github_oauth_callback: %s\n" % e)
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
**302** | Successfully completed the OAuth flow |  * location -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_github_oauth_start**
> user_update_github_oauth_start()

Start OAuth flow

Starts the OAuth flow

### Example


```python
import mtmai.clients.rest
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
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Start OAuth flow
        await api_instance.user_update_github_oauth_start()
    except Exception as e:
        print("Exception when calling UserApi->user_update_github_oauth_start: %s\n" % e)
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
**302** | Successfully started the OAuth flow |  * location -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_google_oauth_callback**
> user_update_google_oauth_callback()

Complete OAuth flow

Completes the OAuth flow

### Example


```python
import mtmai.clients.rest
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
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Complete OAuth flow
        await api_instance.user_update_google_oauth_callback()
    except Exception as e:
        print("Exception when calling UserApi->user_update_google_oauth_callback: %s\n" % e)
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
**302** | Successfully completed the OAuth flow |  * location -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_google_oauth_start**
> user_update_google_oauth_start()

Start OAuth flow

Starts the OAuth flow

### Example


```python
import mtmai.clients.rest
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
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Start OAuth flow
        await api_instance.user_update_google_oauth_start()
    except Exception as e:
        print("Exception when calling UserApi->user_update_google_oauth_start: %s\n" % e)
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
**302** | Successfully started the OAuth flow |  * location -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_login**
> User user_update_login(user_login_request=user_login_request)

Login user

Logs in a user.

### Example


```python
import mtmai.clients.rest
from mtmai.clients.rest.models.user import User
from mtmai.clients.rest.models.user_login_request import UserLoginRequest
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
    api_instance = mtmai.clients.rest.UserApi(api_client)
    user_login_request = mtmai.clients.rest.UserLoginRequest() # UserLoginRequest |  (optional)

    try:
        # Login user
        api_response = await api_instance.user_update_login(user_login_request=user_login_request)
        print("The response of UserApi->user_update_login:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->user_update_login: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_login_request** | [**UserLoginRequest**](UserLoginRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully logged in |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_logout**
> User user_update_logout()

Logout user

Logs out a user.

### Example

* Api Key Authentication (cookieAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.user import User
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

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Logout user
        api_response = await api_instance.user_update_logout()
        print("The response of UserApi->user_update_logout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->user_update_logout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully logged out |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_password**
> User user_update_password(user_change_password_request=user_change_password_request)

Change user password

Update a user password.

### Example

* Api Key Authentication (cookieAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.user import User
from mtmai.clients.rest.models.user_change_password_request import UserChangePasswordRequest
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

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.UserApi(api_client)
    user_change_password_request = mtmai.clients.rest.UserChangePasswordRequest() # UserChangePasswordRequest |  (optional)

    try:
        # Change user password
        api_response = await api_instance.user_update_password(user_change_password_request=user_change_password_request)
        print("The response of UserApi->user_update_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->user_update_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_change_password_request** | [**UserChangePasswordRequest**](UserChangePasswordRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully changed password |  -  |
**400** | A malformed or bad request |  -  |
**401** | Unauthorized |  -  |
**405** | Method not allowed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_slack_oauth_callback**
> user_update_slack_oauth_callback()

Complete OAuth flow

Completes the OAuth flow

### Example

* Api Key Authentication (cookieAuth):

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

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.UserApi(api_client)

    try:
        # Complete OAuth flow
        await api_instance.user_update_slack_oauth_callback()
    except Exception as e:
        print("Exception when calling UserApi->user_update_slack_oauth_callback: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**302** | Successfully completed the OAuth flow |  * location -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_update_slack_oauth_start**
> user_update_slack_oauth_start(tenant)

Start OAuth flow

Starts the OAuth flow

### Example

* Api Key Authentication (cookieAuth):

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

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with mtmai.clients.rest.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = mtmai.clients.rest.UserApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # Start OAuth flow
        await api_instance.user_update_slack_oauth_start(tenant)
    except Exception as e:
        print("Exception when calling UserApi->user_update_slack_oauth_start: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**302** | Successfully started the OAuth flow |  * location -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

