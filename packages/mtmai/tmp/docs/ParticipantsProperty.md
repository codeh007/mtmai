# ParticipantsProperty


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the component. | [optional] 
**provider** | **str** |  | 
**component_type** | **str** |  | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | 
**description** | **str** | Description of the component. | 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | 
**config** | **Dict[str, object]** |  | 

## Example

```python
from mtmai.clients.rest.models.participants_property import ParticipantsProperty

# TODO update the JSON string below
json = "{}"
# create an instance of ParticipantsProperty from a JSON string
participants_property_instance = ParticipantsProperty.from_json(json)
# print the JSON string representation of the object
print(ParticipantsProperty.to_json())

# convert the object into a dict
participants_property_dict = participants_property_instance.to_dict()
# create an instance of ParticipantsProperty from a dict
participants_property_from_dict = ParticipantsProperty.from_dict(participants_property_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


