# APIMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth** | [**APIMetaAuth**](APIMetaAuth.md) |  | [optional] 
**pylon_app_id** | **str** | the Pylon app ID for usepylon.com chat support | [optional] 
**posthog** | [**APIMetaPosthog**](APIMetaPosthog.md) |  | [optional] 
**allow_signup** | **bool** | whether or not users can sign up for this instance | [optional] 
**allow_invites** | **bool** | whether or not users can invite other users to this instance | [optional] 
**allow_create_tenant** | **bool** | whether or not users can create new tenants | [optional] 
**allow_change_password** | **bool** | whether or not users can change their password | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.api_meta import APIMeta

# TODO update the JSON string below
json = "{}"
# create an instance of APIMeta from a JSON string
api_meta_instance = APIMeta.from_json(json)
# print the JSON string representation of the object
print(APIMeta.to_json())

# convert the object into a dict
api_meta_dict = api_meta_instance.to_dict()
# create an instance of APIMeta from a dict
api_meta_from_dict = APIMeta.from_dict(api_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


