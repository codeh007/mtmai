# Subsection


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subsection_title** | **str** | Title of the subsection | 
**description** | **str** | Content of the subsection | 

## Example

```python
from mtmai.clients.rest.models.subsection import Subsection

# TODO update the JSON string below
json = "{}"
# create an instance of Subsection from a JSON string
subsection_instance = Subsection.from_json(json)
# print the JSON string representation of the object
print(Subsection.to_json())

# convert the object into a dict
subsection_dict = subsection_instance.to_dict()
# create an instance of Subsection from a dict
subsection_from_dict = Subsection.from_dict(subsection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


