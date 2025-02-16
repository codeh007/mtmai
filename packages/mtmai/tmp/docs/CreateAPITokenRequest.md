# CreateAPITokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A name for the API token. | 
**expires_in** | **str** | The duration for which the token is valid. | [optional] 

## Example

```python
from mtmai.clients.rest.models.create_api_token_request import CreateAPITokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAPITokenRequest from a JSON string
create_api_token_request_instance = CreateAPITokenRequest.from_json(json)
# print the JSON string representation of the object
print(CreateAPITokenRequest.to_json())

# convert the object into a dict
create_api_token_request_dict = create_api_token_request_instance.to_dict()
# create an instance of CreateAPITokenRequest from a dict
create_api_token_request_from_dict = CreateAPITokenRequest.from_dict(create_api_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


