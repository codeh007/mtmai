# SchemaForm


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**fields** | [**List[FormField]**](FormField.md) |  | 

## Example

```python
from mtmai.clients.rest.models.schema_form import SchemaForm

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaForm from a JSON string
schema_form_instance = SchemaForm.from_json(json)
# print the JSON string representation of the object
print(SchemaForm.to_json())

# convert the object into a dict
schema_form_dict = schema_form_instance.to_dict()
# create an instance of SchemaForm from a dict
schema_form_from_dict = SchemaForm.from_dict(schema_form_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


