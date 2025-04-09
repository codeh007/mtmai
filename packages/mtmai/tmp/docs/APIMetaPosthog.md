# APIMetaPosthog


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | the PostHog API key | [optional] 
**api_host** | **str** | the PostHog API host | [optional] 

## Example

```python
from mtmai.clients.rest.models.api_meta_posthog import APIMetaPosthog

# TODO update the JSON string below
json = "{}"
# create an instance of APIMetaPosthog from a JSON string
api_meta_posthog_instance = APIMetaPosthog.from_json(json)
# print the JSON string representation of the object
print(APIMetaPosthog.to_json())

# convert the object into a dict
api_meta_posthog_dict = api_meta_posthog_instance.to_dict()
# create an instance of APIMetaPosthog from a dict
api_meta_posthog_from_dict = APIMetaPosthog.from_dict(api_meta_posthog_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


