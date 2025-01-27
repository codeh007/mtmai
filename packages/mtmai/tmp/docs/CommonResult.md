# CommonResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** |  | 
**message** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.common_result import CommonResult

# TODO update the JSON string below
json = "{}"
# create an instance of CommonResult from a JSON string
common_result_instance = CommonResult.from_json(json)
# print the JSON string representation of the object
print(CommonResult.to_json())

# convert the object into a dict
common_result_dict = common_result_instance.to_dict()
# create an instance of CommonResult from a dict
common_result_from_dict = CommonResult.from_dict(common_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


