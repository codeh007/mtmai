# WebhookWorkerCreateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**worker** | [**WebhookWorkerCreated**](WebhookWorkerCreated.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.webhook_worker_create_response import WebhookWorkerCreateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorkerCreateResponse from a JSON string
webhook_worker_create_response_instance = WebhookWorkerCreateResponse.from_json(json)
# print the JSON string representation of the object
print(WebhookWorkerCreateResponse.to_json())

# convert the object into a dict
webhook_worker_create_response_dict = webhook_worker_create_response_instance.to_dict()
# create an instance of WebhookWorkerCreateResponse from a dict
webhook_worker_create_response_from_dict = WebhookWorkerCreateResponse.from_dict(webhook_worker_create_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


