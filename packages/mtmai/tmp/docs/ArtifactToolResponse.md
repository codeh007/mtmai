# ArtifactToolResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**artifact** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**language** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.artifact_tool_response import ArtifactToolResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ArtifactToolResponse from a JSON string
artifact_tool_response_instance = ArtifactToolResponse.from_json(json)
# print the JSON string representation of the object
print(ArtifactToolResponse.to_json())

# convert the object into a dict
artifact_tool_response_dict = artifact_tool_response_instance.to_dict()
# create an instance of ArtifactToolResponse from a dict
artifact_tool_response_from_dict = ArtifactToolResponse.from_dict(artifact_tool_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


