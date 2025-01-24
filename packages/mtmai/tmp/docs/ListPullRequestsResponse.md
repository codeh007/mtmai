# ListPullRequestsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pull_requests** | [**List[PullRequest]**](PullRequest.md) |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.list_pull_requests_response import ListPullRequestsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListPullRequestsResponse from a JSON string
list_pull_requests_response_instance = ListPullRequestsResponse.from_json(json)
# print the JSON string representation of the object
print(ListPullRequestsResponse.to_json())

# convert the object into a dict
list_pull_requests_response_dict = list_pull_requests_response_instance.to_dict()
# create an instance of ListPullRequestsResponse from a dict
list_pull_requests_response_from_dict = ListPullRequestsResponse.from_dict(list_pull_requests_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


