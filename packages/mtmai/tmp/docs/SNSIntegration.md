# SNSIntegration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**tenant_id** | **str** | The unique identifier for the tenant that the SNS integration belongs to. | 
**topic_arn** | **str** | The Amazon Resource Name (ARN) of the SNS topic. | 
**ingest_url** | **str** | The URL to send SNS messages to. | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.sns_integration import SNSIntegration

# TODO update the JSON string below
json = "{}"
# create an instance of SNSIntegration from a JSON string
sns_integration_instance = SNSIntegration.from_json(json)
# print the JSON string representation of the object
print(SNSIntegration.to_json())

# convert the object into a dict
sns_integration_dict = sns_integration_instance.to_dict()
# create an instance of SNSIntegration from a dict
sns_integration_from_dict = SNSIntegration.from_dict(sns_integration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


