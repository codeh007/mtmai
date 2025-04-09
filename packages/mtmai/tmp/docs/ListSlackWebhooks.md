# ListSlackWebhooks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | 
**rows** | [**List[SlackWebhook]**](SlackWebhook.md) |  | 

## Example

```python
from mtmai.clients.rest.models.list_slack_webhooks import ListSlackWebhooks

# TODO update the JSON string below
json = "{}"
# create an instance of ListSlackWebhooks from a JSON string
list_slack_webhooks_instance = ListSlackWebhooks.from_json(json)
# print the JSON string representation of the object
print(ListSlackWebhooks.to_json())

# convert the object into a dict
list_slack_webhooks_dict = list_slack_webhooks_instance.to_dict()
# create an instance of ListSlackWebhooks from a dict
list_slack_webhooks_from_dict = ListSlackWebhooks.from_dict(list_slack_webhooks_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


