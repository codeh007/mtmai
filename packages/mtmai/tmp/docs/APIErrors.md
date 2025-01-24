# APIErrors


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[APIError]**](APIError.md) |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.api_errors import APIErrors

# TODO update the JSON string below
json = "{}"
# create an instance of APIErrors from a JSON string
api_errors_instance = APIErrors.from_json(json)
# print the JSON string representation of the object
print(APIErrors.to_json())

# convert the object into a dict
api_errors_dict = api_errors_instance.to_dict()
# create an instance of APIErrors from a dict
api_errors_from_dict = APIErrors.from_dict(api_errors_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


