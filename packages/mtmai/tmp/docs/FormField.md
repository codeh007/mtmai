# FormField


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [default to 'text']
**name** | **str** |  | 
**default_value** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**required** | **bool** |  | [optional] 
**min** | **float** |  | [optional] 
**max** | **float** |  | [optional] 
**placeholder** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.form_field import FormField

# TODO update the JSON string below
json = "{}"
# create an instance of FormField from a JSON string
form_field_instance = FormField.from_json(json)
# print the JSON string representation of the object
print(FormField.to_json())

# convert the object into a dict
form_field_dict = form_field_instance.to_dict()
# create an instance of FormField from a dict
form_field_from_dict = FormField.from_dict(form_field_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


