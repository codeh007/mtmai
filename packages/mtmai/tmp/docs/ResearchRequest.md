# ResearchRequest

研究输入(目前写死为调用社交媒体)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_stream** | **bool** |  | 
**thread_id** | **str** |  | 
**input** | **str** | 详细描述要调研详情 | 

## Example

```python
from mtmai.gomtmclients.rest.models.research_request import ResearchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ResearchRequest from a JSON string
research_request_instance = ResearchRequest.from_json(json)
# print the JSON string representation of the object
print(ResearchRequest.to_json())

# convert the object into a dict
research_request_dict = research_request_instance.to_dict()
# create an instance of ResearchRequest from a dict
research_request_from_dict = ResearchRequest.from_dict(research_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


