# CreateSNSIntegrationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**topic_arn** | **str** | The Amazon Resource Name (ARN) of the SNS topic. | 

## Example

```python
from mtmai.clients.rest.models.create_sns_integration_request import CreateSNSIntegrationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSNSIntegrationRequest from a JSON string
create_sns_integration_request_instance = CreateSNSIntegrationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSNSIntegrationRequest.to_json())

# convert the object into a dict
create_sns_integration_request_dict = create_sns_integration_request_instance.to_dict()
# create an instance of CreateSNSIntegrationRequest from a dict
create_sns_integration_request_from_dict = CreateSNSIntegrationRequest.from_dict(create_sns_integration_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


