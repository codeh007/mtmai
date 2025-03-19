# UserChangePasswordRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**password** | **str** | The password of the user. | 
**new_password** | **str** | The new password for the user. | 

## Example

```python
from mtmai.clients.rest.models.user_change_password_request import UserChangePasswordRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UserChangePasswordRequest from a JSON string
user_change_password_request_instance = UserChangePasswordRequest.from_json(json)
# print the JSON string representation of the object
print(UserChangePasswordRequest.to_json())

# convert the object into a dict
user_change_password_request_dict = user_change_password_request_instance.to_dict()
# create an instance of UserChangePasswordRequest from a dict
user_change_password_request_from_dict = UserChangePasswordRequest.from_dict(user_change_password_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


