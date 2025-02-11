# WebhookWorkerCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the webhook worker. | 
**url** | **str** | The webhook url. | 
**secret** | **str** | The secret key for validation. If not provided, a random secret will be generated. | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.webhook_worker_create_request import WebhookWorkerCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorkerCreateRequest from a JSON string
webhook_worker_create_request_instance = WebhookWorkerCreateRequest.from_json(json)
# print the JSON string representation of the object
print(WebhookWorkerCreateRequest.to_json())

# convert the object into a dict
webhook_worker_create_request_dict = webhook_worker_create_request_instance.to_dict()
# create an instance of WebhookWorkerCreateRequest from a dict
webhook_worker_create_request_from_dict = WebhookWorkerCreateRequest.from_dict(webhook_worker_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


