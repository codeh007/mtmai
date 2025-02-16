# RewriteArtifactMetaToolResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**title** | **str** |  | 
**language** | [**ProgrammingLanguageOptions**](ProgrammingLanguageOptions.md) |  | 

## Example

```python
from mtmai.clients.rest.models.rewrite_artifact_meta_tool_response import RewriteArtifactMetaToolResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RewriteArtifactMetaToolResponse from a JSON string
rewrite_artifact_meta_tool_response_instance = RewriteArtifactMetaToolResponse.from_json(json)
# print the JSON string representation of the object
print(RewriteArtifactMetaToolResponse.to_json())

# convert the object into a dict
rewrite_artifact_meta_tool_response_dict = rewrite_artifact_meta_tool_response_instance.to_dict()
# create an instance of RewriteArtifactMetaToolResponse from a dict
rewrite_artifact_meta_tool_response_from_dict = RewriteArtifactMetaToolResponse.from_dict(rewrite_artifact_meta_tool_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


