# User


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | The display name of the user. | [optional] 
**email** | **str** | The email address of the user. | 
**email_verified** | **bool** | Whether the user has verified their email address. | 
**has_password** | **bool** | Whether the user has a password set. | [optional] 
**email_hash** | **str** | A hash of the user&#39;s email address for use with Pylon Support Chat | [optional] 
**user_token** | **str** | The user&#39;s token for use with Pylon Support Chat | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.user import User

# TODO update the JSON string below
json = "{}"
# create an instance of User from a JSON string
user_instance = User.from_json(json)
# print the JSON string representation of the object
print(User.to_json())

# convert the object into a dict
user_dict = user_instance.to_dict()
# create an instance of User from a dict
user_from_dict = User.from_dict(user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


