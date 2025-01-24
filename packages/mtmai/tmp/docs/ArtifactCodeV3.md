# ArtifactCodeV3


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** |  | 
**type** | **str** |  | 
**title** | **str** |  | 
**language** | [**ProgrammingLanguageOptions**](ProgrammingLanguageOptions.md) |  | 
**code** | **str** |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.artifact_code_v3 import ArtifactCodeV3

# TODO update the JSON string below
json = "{}"
# create an instance of ArtifactCodeV3 from a JSON string
artifact_code_v3_instance = ArtifactCodeV3.from_json(json)
# print the JSON string representation of the object
print(ArtifactCodeV3.to_json())

# convert the object into a dict
artifact_code_v3_dict = artifact_code_v3_instance.to_dict()
# create an instance of ArtifactCodeV3 from a dict
artifact_code_v3_from_dict = ArtifactCodeV3.from_dict(artifact_code_v3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


