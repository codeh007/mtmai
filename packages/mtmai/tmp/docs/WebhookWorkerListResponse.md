# WebhookWorkerListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[WebhookWorker]**](WebhookWorker.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.webhook_worker_list_response import WebhookWorkerListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookWorkerListResponse from a JSON string
webhook_worker_list_response_instance = WebhookWorkerListResponse.from_json(json)
# print the JSON string representation of the object
print(WebhookWorkerListResponse.to_json())

# convert the object into a dict
webhook_worker_list_response_dict = webhook_worker_list_response_instance.to_dict()
# create an instance of WebhookWorkerListResponse from a dict
webhook_worker_list_response_from_dict = WebhookWorkerListResponse.from_dict(webhook_worker_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


