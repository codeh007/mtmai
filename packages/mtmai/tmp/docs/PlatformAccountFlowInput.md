# PlatformAccountFlowInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] [default to 'PlatformAccountFlowInput']
**platform_account_id** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.platform_account_flow_input import PlatformAccountFlowInput

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformAccountFlowInput from a JSON string
platform_account_flow_input_instance = PlatformAccountFlowInput.from_json(json)
# print the JSON string representation of the object
print(PlatformAccountFlowInput.to_json())

# convert the object into a dict
platform_account_flow_input_dict = platform_account_flow_input_instance.to_dict()
# create an instance of PlatformAccountFlowInput from a dict
platform_account_flow_input_from_dict = PlatformAccountFlowInput.from_dict(platform_account_flow_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


