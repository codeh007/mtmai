# CodeHighlight


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_char_index** | **float** |  | 
**end_char_index** | **float** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.code_highlight import CodeHighlight

# TODO update the JSON string below
json = "{}"
# create an instance of CodeHighlight from a JSON string
code_highlight_instance = CodeHighlight.from_json(json)
# print the JSON string representation of the object
print(CodeHighlight.to_json())

# convert the object into a dict
code_highlight_dict = code_highlight_instance.to_dict()
# create an instance of CodeHighlight from a dict
code_highlight_from_dict = CodeHighlight.from_dict(code_highlight_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


