# WebhookWorkerCreated


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | The name of the webhook worker. | 
**url** | **str** | The webhook url. | 
**secret** | **str** | The secret key for validation. | 

## Example

```python
from mtmai.gomtmclients.rest.models.webhook_worker_created import WebhookWorkerCreated

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorkerCreated from a JSON string
webhook_worker_created_instance = WebhookWorkerCreated.from_json(json)
# print the JSON string representation of the object
print(WebhookWorkerCreated.to_json())

# convert the object into a dict
webhook_worker_created_dict = webhook_worker_created_instance.to_dict()
# create an instance of WebhookWorkerCreated from a dict
webhook_worker_created_from_dict = WebhookWorkerCreated.from_dict(webhook_worker_created_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


