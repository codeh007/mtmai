# OutlineSectionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**section_title** | **str** | Title of the section | 
**description** | **str** | Content of the section | 
**subsections** | [**List[OutlineSectionsInnerSubsectionsInner]**](OutlineSectionsInnerSubsectionsInner.md) | Titles and descriptions for each subsection of the Wikipedia page | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.outline_sections_inner import OutlineSectionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of OutlineSectionsInner from a JSON string
outline_sections_inner_instance = OutlineSectionsInner.from_json(json)
# print the JSON string representation of the object
print(OutlineSectionsInner.to_json())

# convert the object into a dict
outline_sections_inner_dict = outline_sections_inner_instance.to_dict()
# create an instance of OutlineSectionsInner from a dict
outline_sections_inner_from_dict = OutlineSectionsInner.from_dict(outline_sections_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


