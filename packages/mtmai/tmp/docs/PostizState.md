# PostizState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel** | [**PostizChannel**](PostizChannel.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.postiz_state import PostizState

# TODO update the JSON string below
json = "{}"
# create an instance of PostizState from a JSON string
postiz_state_instance = PostizState.from_json(json)
# print the JSON string representation of the object
print(PostizState.to_json())

# convert the object into a dict
postiz_state_dict = postiz_state_instance.to_dict()
# create an instance of PostizState from a dict
postiz_state_from_dict = PostizState.from_dict(postiz_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


