# WebSearchResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | 结果描述 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.web_search_result import WebSearchResult

# TODO update the JSON string below
json = "{}"
# create an instance of WebSearchResult from a JSON string
web_search_result_instance = WebSearchResult.from_json(json)
# print the JSON string representation of the object
print(WebSearchResult.to_json())

# convert the object into a dict
web_search_result_dict = web_search_result_instance.to_dict()
# create an instance of WebSearchResult from a dict
web_search_result_from_dict = WebSearchResult.from_dict(web_search_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


