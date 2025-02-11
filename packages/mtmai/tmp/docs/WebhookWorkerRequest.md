# WebhookWorkerRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | The date and time the request was created. | 
**method** | [**WebhookWorkerRequestMethod**](WebhookWorkerRequestMethod.md) | The HTTP method used for the request. | 
**status_code** | **int** | The HTTP status code of the response. | 

## Example

```python
from mtmaisdk.clients.rest.models.webhook_worker_request import WebhookWorkerRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorkerRequest from a JSON string
webhook_worker_request_instance = WebhookWorkerRequest.from_json(json)
# print the JSON string representation of the object
print(WebhookWorkerRequest.to_json())

# convert the object into a dict
webhook_worker_request_dict = webhook_worker_request_instance.to_dict()
# create an instance of WebhookWorkerRequest from a dict
webhook_worker_request_from_dict = WebhookWorkerRequest.from_dict(webhook_worker_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


