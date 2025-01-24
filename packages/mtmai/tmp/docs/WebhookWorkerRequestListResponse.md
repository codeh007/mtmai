# WebhookWorkerRequestListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requests** | [**List[WebhookWorkerRequest]**](WebhookWorkerRequest.md) | The list of webhook requests. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.webhook_worker_request_list_response import WebhookWorkerRequestListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorkerRequestListResponse from a JSON string
webhook_worker_request_list_response_instance = WebhookWorkerRequestListResponse.from_json(json)
# print the JSON string representation of the object
print(WebhookWorkerRequestListResponse.to_json())

# convert the object into a dict
webhook_worker_request_list_response_dict = webhook_worker_request_list_response_instance.to_dict()
# create an instance of WebhookWorkerRequestListResponse from a dict
webhook_worker_request_list_response_from_dict = WebhookWorkerRequestListResponse.from_dict(webhook_worker_request_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


