# OperataionGuideResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | 详细的操作手册描述 | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.operataion_guide_response import OperataionGuideResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OperataionGuideResponse from a JSON string
operataion_guide_response_instance = OperataionGuideResponse.from_json(json)
# print the JSON string representation of the object
print(OperataionGuideResponse.to_json())

# convert the object into a dict
operataion_guide_response_dict = operataion_guide_response_instance.to_dict()
# create an instance of OperataionGuideResponse from a dict
operataion_guide_response_from_dict = OperataionGuideResponse.from_dict(operataion_guide_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


