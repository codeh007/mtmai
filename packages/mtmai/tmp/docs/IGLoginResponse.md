# IGLoginResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.ig_login_response import IGLoginResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IGLoginResponse from a JSON string
ig_login_response_instance = IGLoginResponse.from_json(json)
# print the JSON string representation of the object
print(IGLoginResponse.to_json())

# convert the object into a dict
ig_login_response_dict = ig_login_response_instance.to_dict()
# create an instance of IGLoginResponse from a dict
ig_login_response_from_dict = IGLoginResponse.from_dict(ig_login_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


