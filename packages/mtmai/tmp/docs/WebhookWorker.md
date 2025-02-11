# WebhookWorker


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | The name of the webhook worker. | 
**url** | **str** | The webhook url. | 

## Example

```python
from mtmaisdk.clients.rest.models.webhook_worker import WebhookWorker

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorker from a JSON string
webhook_worker_instance = WebhookWorker.from_json(json)
# print the JSON string representation of the object
print(WebhookWorker.to_json())

# convert the object into a dict
webhook_worker_dict = webhook_worker_instance.to_dict()
# create an instance of WebhookWorker from a dict
webhook_worker_from_dict = WebhookWorker.from_dict(webhook_worker_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


