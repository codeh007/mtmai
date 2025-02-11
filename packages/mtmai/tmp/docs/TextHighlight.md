# TextHighlight


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_markdown** | **str** |  | 
**markdown_block** | **str** |  | 
**selected_text** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.text_highlight import TextHighlight

# TODO update the JSON string below
json = "{}"
# create an instance of TextHighlight from a JSON string
text_highlight_instance = TextHighlight.from_json(json)
# print the JSON string representation of the object
print(TextHighlight.to_json())

# convert the object into a dict
text_highlight_dict = text_highlight_instance.to_dict()
# create an instance of TextHighlight from a dict
text_highlight_from_dict = TextHighlight.from_dict(text_highlight_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


