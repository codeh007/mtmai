# RequestUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_tokens** | **float** |  | 
**completion_tokens** | **float** |  | 

## Example

```python
from mtmai.clients.rest.models.request_usage import RequestUsage

# TODO update the JSON string below
json = "{}"
# create an instance of RequestUsage from a JSON string
request_usage_instance = RequestUsage.from_json(json)
# print the JSON string representation of the object
print(RequestUsage.to_json())

# convert the object into a dict
request_usage_dict = request_usage_instance.to_dict()
# create an instance of RequestUsage from a dict
request_usage_from_dict = RequestUsage.from_dict(request_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


