# mtmai.clients.rest.EventApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**event_create**](EventApi.md#event_create) | **POST** /api/v1/tenants/{tenant}/events | Create event
[**event_create_bulk**](EventApi.md#event_create_bulk) | **POST** /api/v1/tenants/{tenant}/events/bulk | Bulk Create events
[**event_data_get**](EventApi.md#event_data_get) | **GET** /api/v1/events/{event}/data | Get event data
[**event_get**](EventApi.md#event_get) | **GET** /api/v1/events/{event} | Get event data
[**event_key_list**](EventApi.md#event_key_list) | **GET** /api/v1/tenants/{tenant}/events/keys | List event keys
[**event_list**](EventApi.md#event_list) | **GET** /api/v1/tenants/{tenant}/events | List events
[**event_update_cancel**](EventApi.md#event_update_cancel) | **POST** /api/v1/tenants/{tenant}/events/cancel | Replay events
[**event_update_replay**](EventApi.md#event_update_replay) | **POST** /api/v1/tenants/{tenant}/events/replay | Replay events


# **event_create**
> Event event_create(tenant, create_event_request)

Create event

Creates a new event.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.create_event_request import CreateEventRequest
from mtmai.clients.rest.models.event import Event
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    create_event_request = mtmai.clients.rest.CreateEventRequest() # CreateEventRequest | The event to create

    try:
        # Create event
        api_response = await api_instance.event_create(tenant, create_event_request)
        print("The response of EventApi->event_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **create_event_request** | [**CreateEventRequest**](CreateEventRequest.md)| The event to create | 

### Return type

[**Event**](Event.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the event |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**429** | Resource limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_create_bulk**
> BulkCreateEventResponse event_create_bulk(tenant, bulk_create_event_request)

Bulk Create events

Bulk creates new events.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.bulk_create_event_request import BulkCreateEventRequest
from mtmai.clients.rest.models.bulk_create_event_response import BulkCreateEventResponse
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    bulk_create_event_request = mtmai.clients.rest.BulkCreateEventRequest() # BulkCreateEventRequest | The events to create

    try:
        # Bulk Create events
        api_response = await api_instance.event_create_bulk(tenant, bulk_create_event_request)
        print("The response of EventApi->event_create_bulk:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_create_bulk: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **bulk_create_event_request** | [**BulkCreateEventRequest**](BulkCreateEventRequest.md)| The events to create | 

### Return type

[**BulkCreateEventResponse**](BulkCreateEventResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**429** | Resource limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_data_get**
> EventData event_data_get(event)

Get event data

Get the data for an event.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.event_data import EventData
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    event = 'event_example' # str | The event id

    try:
        # Get event data
        api_response = await api_instance.event_data_get(event)
        print("The response of EventApi->event_data_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_data_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event** | **str**| The event id | 

### Return type

[**EventData**](EventData.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the event data |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_get**
> Event event_get(event)

Get event data

Get an event.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.event import Event
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    event = 'event_example' # str | The event id

    try:
        # Get event data
        api_response = await api_instance.event_get(event)
        print("The response of EventApi->event_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event** | **str**| The event id | 

### Return type

[**Event**](Event.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the event data |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_key_list**
> EventKeyList event_key_list(tenant)

List event keys

Lists all event keys for a tenant.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.event_key_list import EventKeyList
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    tenant = 'tenant_example' # str | The tenant id

    try:
        # List event keys
        api_response = await api_instance.event_key_list(tenant)
        print("The response of EventApi->event_key_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_key_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 

### Return type

[**EventKeyList**](EventKeyList.md)

### Authorization

[basicAuth](../README.md#basicAuth), [cookieAuth](../README.md#cookieAuth), [bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed the event keys |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_list**
> EventList event_list(tenant, offset=offset, limit=limit, keys=keys, workflows=workflows, statuses=statuses, search=search, order_by_field=order_by_field, order_by_direction=order_by_direction, additional_metadata=additional_metadata, event_ids=event_ids)

List events

Lists all events for a tenant.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.event_list import EventList
from mtmai.clients.rest.models.event_order_by_direction import EventOrderByDirection
from mtmai.clients.rest.models.event_order_by_field import EventOrderByField
from mtmai.clients.rest.models.workflow_run_status import WorkflowRunStatus
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    offset = 56 # int | The number to skip (optional)
    limit = 56 # int | The number to limit by (optional)
    keys = ['keys_example'] # List[str] | A list of keys to filter by (optional)
    workflows = ['workflows_example'] # List[str] | A list of workflow IDs to filter by (optional)
    statuses = [mtmai.clients.rest.WorkflowRunStatus()] # List[WorkflowRunStatus] | A list of workflow run statuses to filter by (optional)
    search = 'search_example' # str | The search query to filter for (optional)
    order_by_field = mtmai.clients.rest.EventOrderByField() # EventOrderByField | What to order by (optional)
    order_by_direction = mtmai.clients.rest.EventOrderByDirection() # EventOrderByDirection | The order direction (optional)
    additional_metadata = ['[key1:value1, key2:value2]'] # List[str] | A list of metadata key value pairs to filter by (optional)
    event_ids = ['event_ids_example'] # List[str] | A list of event ids to filter by (optional)

    try:
        # List events
        api_response = await api_instance.event_list(tenant, offset=offset, limit=limit, keys=keys, workflows=workflows, statuses=statuses, search=search, order_by_field=order_by_field, order_by_direction=order_by_direction, additional_metadata=additional_metadata, event_ids=event_ids)
        print("The response of EventApi->event_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **offset** | **int**| The number to skip | [optional] 
 **limit** | **int**| The number to limit by | [optional] 
 **keys** | [**List[str]**](str.md)| A list of keys to filter by | [optional] 
 **workflows** | [**List[str]**](str.md)| A list of workflow IDs to filter by | [optional] 
 **statuses** | [**List[WorkflowRunStatus]**](WorkflowRunStatus.md)| A list of workflow run statuses to filter by | [optional] 
 **search** | **str**| The search query to filter for | [optional] 
 **order_by_field** | [**EventOrderByField**](.md)| What to order by | [optional] 
 **order_by_direction** | [**EventOrderByDirection**](.md)| The order direction | [optional] 
 **additional_metadata** | [**List[str]**](str.md)| A list of metadata key value pairs to filter by | [optional] 
 **event_ids** | [**List[str]**](str.md)| A list of event ids to filter by | [optional] 

### Return type

[**EventList**](EventList.md)

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

# **event_update_cancel**
> EventUpdateCancel200Response event_update_cancel(tenant, cancel_event_request)

Replay events

Cancels all runs for a list of events.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.cancel_event_request import CancelEventRequest
from mtmai.clients.rest.models.event_update_cancel200_response import EventUpdateCancel200Response
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    cancel_event_request = mtmai.clients.rest.CancelEventRequest() # CancelEventRequest | The event ids to replay

    try:
        # Replay events
        api_response = await api_instance.event_update_cancel(tenant, cancel_event_request)
        print("The response of EventApi->event_update_cancel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_update_cancel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **cancel_event_request** | [**CancelEventRequest**](CancelEventRequest.md)| The event ids to replay | 

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
**200** | Successfully canceled runs for the events |  -  |
**400** | A malformed or bad request |  -  |
**403** | Forbidden |  -  |
**429** | Resource limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_update_replay**
> EventList event_update_replay(tenant, replay_event_request)

Replay events

Replays a list of events.

### Example

* Basic Authentication (basicAuth):
* Api Key Authentication (cookieAuth):
* Bearer Authentication (bearerAuth):

```python
import mtmai.clients.rest
from mtmai.clients.rest.models.event_list import EventList
from mtmai.clients.rest.models.replay_event_request import ReplayEventRequest
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
    api_instance = mtmai.clients.rest.EventApi(api_client)
    tenant = 'tenant_example' # str | The tenant id
    replay_event_request = mtmai.clients.rest.ReplayEventRequest() # ReplayEventRequest | The event ids to replay

    try:
        # Replay events
        api_response = await api_instance.event_update_replay(tenant, replay_event_request)
        print("The response of EventApi->event_update_replay:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EventApi->event_update_replay: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tenant** | **str**| The tenant id | 
 **replay_event_request** | [**ReplayEventRequest**](ReplayEventRequest.md)| The event ids to replay | 

### Return type

[**EventList**](EventList.md)

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
**429** | Resource limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

