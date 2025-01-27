# HfAccount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**username** | **str** | The username of the hf account. | 
**token** | **str** | The token of the hf account. | 

## Example

```python
from mtmaisdk.clients.rest.models.hf_account import HfAccount

# TODO update the JSON string below
json = "{}"
# create an instance of HfAccount from a JSON string
hf_account_instance = HfAccount.from_json(json)
# print the JSON string representation of the object
print(HfAccount.to_json())

# convert the object into a dict
hf_account_dict = hf_account_instance.to_dict()
# create an instance of HfAccount from a dict
hf_account_from_dict = HfAccount.from_dict(hf_account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


