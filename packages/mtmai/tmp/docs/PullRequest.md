# PullRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repository_owner** | **str** |  | 
**repository_name** | **str** |  | 
**pull_request_id** | **int** |  | 
**pull_request_title** | **str** |  | 
**pull_request_number** | **int** |  | 
**pull_request_head_branch** | **str** |  | 
**pull_request_base_branch** | **str** |  | 
**pull_request_state** | [**PullRequestState**](PullRequestState.md) |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.pull_request import PullRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PullRequest from a JSON string
pull_request_instance = PullRequest.from_json(json)
# print the JSON string representation of the object
print(PullRequest.to_json())

# convert the object into a dict
pull_request_dict = pull_request_instance.to_dict()
# create an instance of PullRequest from a dict
pull_request_from_dict = PullRequest.from_dict(pull_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


