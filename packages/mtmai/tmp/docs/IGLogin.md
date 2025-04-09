# IGLogin


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**twofa_code** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.ig_login import IGLogin

# TODO update the JSON string below
json = "{}"
# create an instance of IGLogin from a JSON string
ig_login_instance = IGLogin.from_json(json)
# print the JSON string representation of the object
print(IGLogin.to_json())

# convert the object into a dict
ig_login_dict = ig_login_instance.to_dict()
# create an instance of IGLogin from a dict
ig_login_from_dict = IGLogin.from_dict(ig_login_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


