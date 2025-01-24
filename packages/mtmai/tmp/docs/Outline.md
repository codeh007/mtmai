# Outline


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page_title** | **str** | Title of the Wikipedia page | 
**sections** | [**List[OutlineSectionsInner]**](OutlineSectionsInner.md) | Titles and descriptions for each section of the Wikipedia page | 

## Example

```python
from mtmai.gomtmclients.rest.models.outline import Outline

# TODO update the JSON string below
json = "{}"
# create an instance of Outline from a JSON string
outline_instance = Outline.from_json(json)
# print the JSON string representation of the object
print(Outline.to_json())

# convert the object into a dict
outline_dict = outline_instance.to_dict()
# create an instance of Outline from a dict
outline_from_dict = Outline.from_dict(outline_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


