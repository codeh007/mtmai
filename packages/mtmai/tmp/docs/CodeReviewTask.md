# CodeReviewTask


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session_id** | **str** |  | 
**code_writing_task** | **str** |  | 
**code_writing_scratchpad** | **str** |  | 
**code** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.code_review_task import CodeReviewTask

# TODO update the JSON string below
json = "{}"
# create an instance of CodeReviewTask from a JSON string
code_review_task_instance = CodeReviewTask.from_json(json)
# print the JSON string representation of the object
print(CodeReviewTask.to_json())

# convert the object into a dict
code_review_task_dict = code_review_task_instance.to_dict()
# create an instance of CodeReviewTask from a dict
code_review_task_from_dict = CodeReviewTask.from_dict(code_review_task_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


