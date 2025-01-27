# ArtifactMarkdownV3


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** |  | 
**type** | **str** |  | 
**title** | **str** |  | 
**full_markdown** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.artifact_markdown_v3 import ArtifactMarkdownV3

# TODO update the JSON string below
json = "{}"
# create an instance of ArtifactMarkdownV3 from a JSON string
artifact_markdown_v3_instance = ArtifactMarkdownV3.from_json(json)
# print the JSON string representation of the object
print(ArtifactMarkdownV3.to_json())

# convert the object into a dict
artifact_markdown_v3_dict = artifact_markdown_v3_instance.to_dict()
# create an instance of ArtifactMarkdownV3 from a dict
artifact_markdown_v3_from_dict = ArtifactMarkdownV3.from_dict(artifact_markdown_v3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


