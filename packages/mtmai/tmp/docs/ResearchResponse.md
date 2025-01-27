# ResearchResponse

研究输出(目前写死为调用社交媒体)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**output** | **str** | 研究结果 | 

## Example

```python
from mtmaisdk.clients.rest.models.research_response import ResearchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResearchResponse from a JSON string
research_response_instance = ResearchResponse.from_json(json)
# print the JSON string representation of the object
print(ResearchResponse.to_json())

# convert the object into a dict
research_response_dict = research_response_instance.to_dict()
# create an instance of ResearchResponse from a dict
research_response_from_dict = ResearchResponse.from_dict(research_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


