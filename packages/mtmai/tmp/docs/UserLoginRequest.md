# UserLoginRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email address of the user. | 
**password** | **str** | The password of the user. | 

## Example

```python
from mtmai.clients.rest.models.user_login_request import UserLoginRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UserLoginRequest from a JSON string
user_login_request_instance = UserLoginRequest.from_json(json)
# print the JSON string representation of the object
print(UserLoginRequest.to_json())

# convert the object into a dict
user_login_request_dict = user_login_request_instance.to_dict()
# create an instance of UserLoginRequest from a dict
user_login_request_from_dict = UserLoginRequest.from_dict(user_login_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


