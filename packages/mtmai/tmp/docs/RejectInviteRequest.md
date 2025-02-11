# RejectInviteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invite** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.reject_invite_request import RejectInviteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RejectInviteRequest from a JSON string
reject_invite_request_instance = RejectInviteRequest.from_json(json)
# print the JSON string representation of the object
print(RejectInviteRequest.to_json())

# convert the object into a dict
reject_invite_request_dict = reject_invite_request_instance.to_dict()
# create an instance of RejectInviteRequest from a dict
reject_invite_request_from_dict = RejectInviteRequest.from_dict(reject_invite_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


