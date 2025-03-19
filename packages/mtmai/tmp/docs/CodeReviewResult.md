# CodeReviewResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**review** | **str** |  | 
**session_id** | **str** |  | 
**approved** | **bool** |  | 

## Example

```python
from mtmai.clients.rest.models.code_review_result import CodeReviewResult

# TODO update the JSON string below
json = "{}"
# create an instance of CodeReviewResult from a JSON string
code_review_result_instance = CodeReviewResult.from_json(json)
# print the JSON string representation of the object
print(CodeReviewResult.to_json())

# convert the object into a dict
code_review_result_dict = code_review_result_instance.to_dict()
# create an instance of CodeReviewResult from a dict
code_review_result_from_dict = CodeReviewResult.from_dict(code_review_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


