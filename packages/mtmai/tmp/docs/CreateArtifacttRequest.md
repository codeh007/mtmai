# CreateArtifacttRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**art_id** | **str** | The blog id. | 
**title** | **str** |  | 
**state** | **object** | The tenant associated with this tenant blog. | 

## Example

```python
from mtmai.gomtmclients.rest.models.create_artifactt_request import CreateArtifacttRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateArtifacttRequest from a JSON string
create_artifactt_request_instance = CreateArtifacttRequest.from_json(json)
# print the JSON string representation of the object
print(CreateArtifacttRequest.to_json())

# convert the object into a dict
create_artifactt_request_dict = create_artifactt_request_instance.to_dict()
# create an instance of CreateArtifacttRequest from a dict
create_artifactt_request_from_dict = CreateArtifacttRequest.from_dict(create_artifactt_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


