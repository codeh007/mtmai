# SlackWebhook


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** | The unique identifier for the tenant that the SNS integration belongs to. | 
**team_name** | **str** | The team name associated with this slack webhook. | 
**team_id** | **str** | The team id associated with this slack webhook. | 
**channel_name** | **str** | The channel name associated with this slack webhook. | 
**channel_id** | **str** | The channel id associated with this slack webhook. | 

## Example

```python
from mtmai.gomtmclients.rest.models.slack_webhook import SlackWebhook

# TODO update the JSON string below
json = "{}"
# create an instance of SlackWebhook from a JSON string
slack_webhook_instance = SlackWebhook.from_json(json)
# print the JSON string representation of the object
print(SlackWebhook.to_json())

# convert the object into a dict
slack_webhook_dict = slack_webhook_instance.to_dict()
# create an instance of SlackWebhook from a dict
slack_webhook_from_dict = SlackWebhook.from_dict(slack_webhook_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


